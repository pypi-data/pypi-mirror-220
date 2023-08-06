import torch
import torch.nn as nn
import numpy as np
import time
from .truncated_gauss import TruncatedNormal

class CVAE(nn.Module):

    def __init__(self, input_dim, par_dim, latent_dim, fc_layers = [], conv_layers = [], stride = 1, device="cpu", dropout=0.1, fdim=0, inchannels = 1, dist_type = "gaussian"):
        """
        args
        ----------
        input_dim: int
            length of input time series
        par_dim: int
            size of hidden layers in all encoders
        latent_dim: int
            number of variables in latent space
        par_dim: int
            number of parameter to estimat
        fc_layers: list
            [num_neurons_layer_1, num_neurons_layer_2,....]
        conv_layers: list
            [(num_filters, conv_size, dilation, maxpool size), (...), (...)]
        """
        super().__init__()
        # define useful variables of network
        self.device = device
        self.input_dim = input_dim
        self.par_dim = par_dim
        self.output_dim = self.input_dim + self.par_dim
        self.gauss_par_dim = self.par_dim - 1
        self.latent_dim = latent_dim
        self.inchannels = inchannels
        self.dist_type = dist_type

        # convolutional parts
        self.fc_layers = fc_layers
        #self.fc_layers_decoder = np.array(0.5*np.array(fc_layers[:3])).astype(int)
        self.conv_layers = conv_layers
        self.num_conv = len(self.conv_layers)
        self.stride = stride

        self.trunc_mins = torch.Tensor([0,0,0,0]).to(self.device)
        self.trunc_maxs = torch.Tensor([1,1,1,1]).to(self.device)
        self.activation = nn.ReLU()
        self.tanh = nn.Tanh()
        self.sigmoid = nn.Sigmoid()
        self.drop = nn.Dropout(p=dropout)

        self.small_const = 1e-6
        
        self.fdim = fdim
        
        # encoder r1(z|y) 
        self.rencoder_conv, self.rencoder_lin, _ctr = self.create_network("r", self.input_dim, self.latent_dim, append_dim=self.fdim, fc_layers = self.fc_layers, conv_layers = self.conv_layers)

        # conv layers not used for next two networks, they both use the same rencoder
        # encoder q(z|x, y) 
        qencoder_conv, self.qencoder_lin, self.conv_track_network = self.create_network("q", self.input_dim, self.latent_dim, append_dim=self.par_dim + self.fdim, fc_layers = self.fc_layers, conv_layers = self.conv_layers, track_conv = True)

        # decoder r2(x|z, y) 
        decoder_conv, self.decoder_lin, _ctr = self.create_network("d", self.input_dim, self.par_dim, append_dim=self.latent_dim + self.fdim, fc_layers = self.fc_layers, conv_layers = self.conv_layers, meansize = self.output_dim)
        
    def create_network(self, name, input_dim, output_dim, append_dim=0, mean=True, variance=True, weight = False,fc_layers=[], conv_layers=[], meansize = None, track_conv = False):
        """ Generate arbritrary network, with convolutional layers or not
        args
        ------
        name: str
            name of network
        input_dim: int
            size of input to network
        output_dim: int
            size of output of network
        append_dim: int (optional)
            number of neurons to append to fully connected layers after convolutional layers
        mean: bool (optional) 
            if True adds extra output layer for means 
        variance : bool (optional)
            if True adds extra layer of outputs for variances
        fc_layers: list
            list of fully connected layers, format: [64,64,...] = [num_neurons_layer1, num_neurons_layer2, .....]
        conv_layers: list
            list of convolutional layers, format:[(8,8,2,1), (8,8,2,1)] = [(num_filt1, conv_size1, max_pool_size1, dilation1), (num_filt2, conv_size2, max_pool_size2, dilation2)] 
        """
        conv_network = nn.Sequential() # initialise networks
        conv_track_network = nn.Sequential()
        lin_network = nn.Sequential()
        layer_out_sizes = []
        num_conv = len(conv_layers)
        num_fc = len(fc_layers)
        inchannels = self.inchannels
        insize = self.input_dim
        # add convolutional layers
        for i in range(num_conv):
            padding = int(conv_layers[i][1]/2.) # padding half width
            maxpool = nn.MaxPool1d(conv_layers[i][3]) #define max pooling for this layer
            # add convolutional/activation/maxpooling layers
            conv_network.add_module("r_conv{}".format(i),module = nn.Conv1d(inchannels, conv_layers[i][0], conv_layers[i][1], stride = self.stride,padding=padding, dilation = conv_layers[i][2]))    
            #conv_network.add_module("batch_norm_conv{}".format(i), module = nn.BatchNorm1d(conv_layers[i][0]))
            conv_network.add_module("act_r_conv{}".format(i), module = self.activation)
            conv_network.add_module("pool_r_conv{}".format(i),module = maxpool)
            # define the output size of the layer
            outsize = int(self.conv_out_size(insize, padding, conv_layers[i][2], conv_layers[i][1], self.stride)/conv_layers[i][3]) # output of one filter
            layer_out_sizes.append((conv_layers[i][0],outsize))
            insize = outsize
            inchannels = conv_layers[i][0]

        if track_conv:
            layer_track_out_sizes = []
            num_conv_track = 1
            inchannels_track = 1
            insize_track = self.input_dim
            conv_layers_track = [(4,3,1,16),]

            for i in range(num_conv_track):
                padding = int(conv_layers_track[i][1]/2.) # padding half width
                maxpool_track = nn.MaxPool1d(conv_layers_track[i][3]) #define max pooling for this layer
                # add convolutional/activation/maxpooling layers
                conv_track_network.add_module("r_conv{}".format(i),module = nn.Conv1d(inchannels_track, conv_layers_track[i][0], conv_layers_track[i][1], stride = self.stride,padding=padding, dilation = conv_layers_track[i][2]))    
                conv_track_network.add_module("act_r_conv{}".format(i), module = self.activation)
                #conv_network.add_module("batch_norm_conv{}".format(i), module = nn.BatchNorm1d(conv_layers[i][0]))
                conv_track_network.add_module("pool_r_conv{}".format(i),module = maxpool_track)
                # define the output size of the layer
                outsize_track = int(self.conv_out_size(insize_track, padding, conv_layers_track[i][2], conv_layers_track[i][1], self.stride)/conv_layers_track[i][3]) # output of one filter
                layer_track_out_sizes.append((conv_layers_track[i][0],outsize_track))
                insize_track = outsize_track
                inchannels_track = conv_layers_track[i][0]

            track_append_size = np.prod(layer_track_out_sizes[-1])
            append_dim += track_append_size

        # define the input size to fully connected layer
        lin_input_size = np.prod(layer_out_sizes[-1]) if num_conv > 0 else self.input_dim
        if append_dim:
            lin_input_size += append_dim
        
        layer_size = int(lin_input_size)
        # hidden layers
        for i in range(num_fc):
            lin_network.add_module("r_lin{}".format(i),module=nn.Linear(layer_size, fc_layers[i]))
            #lin_network.add_module("batch_norm_lin{}".format(i), module = nn.BatchNorm1d(fc_layers[i]))
            lin_network.add_module("r_drop{}".format(i),module=self.drop)
            lin_network.add_module("act_r_lin{}".format(i),module=self.activation)
            layer_size = fc_layers[i]
        # output mean and variance of gaussian with size of latent space

        if mean:
            if meansize is None:
                meansize = output_dim
            setattr(self,"mu_{}".format(name[0]),nn.Linear(layer_size, meansize))
        if variance:
            setattr(self,"log_var_{}".format(name[0]),nn.Linear(layer_size, output_dim))
        if self.dist_type is not "gaussian":
            if weight:
                setattr(self,"weight_{}".format(name[0]),nn.Linear(layer_size, 1))

        return conv_network, lin_network, conv_track_network

    def conv_out_size(self, in_dim, padding, dilation, kernel, stride):
        """ Get output size of a convolutional layer (or one filter from that layer)"""
        return int((in_dim + 2*padding - dilation*(kernel-1)-1)/stride + 1)
        
    def encode_r(self,y, freqs):
        """ encoder r1(z|y) , takes in observation y"""
        conv = self.rencoder_conv(torch.reshape(y, (y.size(0), self.inchannels, self.input_dim))) if self.num_conv > 0 else y
        lin_in = torch.flatten(conv,start_dim=1)
        if freqs is not None:
            lin_in = torch.cat([lin_in, torch.unsqueeze(freqs, 1)],1)
        lin = self.rencoder_lin(lin_in)
        z_mu = self.mu_r(lin) # latent means
        z_log_var = self.log_var_r(lin) + self.small_const # latent variances
        return z_mu, z_log_var
    
    def encode_q(self,y,par, freqs):
        """ encoder q(z|x, y) , takes in observation y and paramters par (x)"""
        conv = self.rencoder_conv(torch.reshape(y, (y.size(0), self.inchannels, self.input_dim))) if self.num_conv > 0 else y
        conv_track = self.conv_track_network(torch.reshape(par[:,4:], (par.size(0), 1, self.input_dim)))
        par = torch.cat([torch.flatten(conv_track,start_dim=1), par[:,:4]],1)
        lin_in = torch.cat([torch.flatten(conv,start_dim=1), par],1)
        if freqs is not None:
            lin_in = torch.cat([lin_in, torch.unsqueeze(freqs, 1)],1)
        lin = self.qencoder_lin(lin_in)
        z_mu = self.mu_q(lin)  # latent means
        z_log_var = self.log_var_q(lin) + self.small_const # latent vairances
        return z_mu, z_log_var
    
    def decode(self, z, y, freqs):
        """ decoder r2(x|z, y) , takes in observation y and latent paramters z"""
        conv = self.rencoder_conv(torch.reshape(y, (y.size(0), self.inchannels, self.input_dim))) if self.num_conv > 0 else y
        lin_in = torch.cat([torch.flatten(conv,start_dim=1),z],1) 
        if freqs is not None:
            lin_in = torch.cat([lin_in, torch.unsqueeze(freqs, 1)],1)
        lin = self.decoder_lin(lin_in)
        par_mu = self.mu_d(lin) # parameter means
        par_mu[:,:4] = self.sigmoid(par_mu[:,:4])
        #par_mu[:,:3] = self.sigmoid(par_mu[:,:3])
        par_log_var = self.log_var_d(lin) + self.small_const # parameter variances
        return par_mu, par_log_var

    def gauss_sample(self, mean, log_var, num_batch, dim):
        """ Sample trom a gaussian with given mean and log variance 
        (takes in a number (dim) of means and variances, and samples num_batch times)"""
        std = torch.exp(0.5 * (log_var))
        eps = torch.randn([num_batch, dim]).to(self.device)
        sample = torch.add(torch.mul(eps,std),mean)
        return sample

    def trunc_gauss_sample(self, mu, log_var, ramp = 1.0):
        """Gaussian log-likelihood """
        sigma = torch.sqrt(torch.exp(log_var))
        #dist = TruncatedNormal(mu, sigma, self.trunc_mins - 10 + ramp*10, self.trunc_maxs + 10 - ramp*10)
        dist = TruncatedNormal(mu, sigma, 0, 1)
        return dist.sample()

    def log_likelihood_trunc_gauss(self,par, mu, log_var, ramp = 1.0):
        """Gaussian log-likelihood """
        sigma = torch.sqrt(torch.exp(log_var))
        try:
            #dist = TruncatedNormal(mu, sigma, a=self.trunc_mins - 10 + ramp*10, b=self.trunc_maxs + 10 - ramp*10)
            dist = TruncatedNormal(mu, sigma, a=0, b=1)
        except:
            #print((self.trunc_mins - 10 + ramp*10 - mu)/sigma, (self.trunc_maxs + 10 - ramp*10 - mu)/sigma, ramp*10
            print(mu)
        return dist.log_prob(par)

    def log_likelihood_cat(self, par, logits):
        """Gaussian log-likelihood """ 
        cat = torch.distributions.binomial.Binomial(total_count = 1, logits = logits)
        logliks = cat.log_prob(par)
        # takes the mean of the likelihoods in the parameter space
        return logliks

    def cat_samp(self, logits):
        cat = torch.distributions.binomial.Binomial(total_count = 1, logits = logits)
        return cat.sample()
    
    def KL_gauss(self,mu_r,log_var_r,mu_q,log_var_q):
        """Gaussian KL divergence between two distributions"""
        sigma_q = torch.exp(0.5 * (log_var_q))
        sigma_r = torch.exp(0.5 * (log_var_r))
        t2 = torch.log(sigma_r/sigma_q)
        t3 = (torch.square(mu_q - mu_r) + torch.square(sigma_q))/(2*torch.square(sigma_r))
        # take sum of KL divergences in the latent space
        kl_loss = torch.sum(t2 + t3 - 0.5,dim=1)
        return kl_loss


    def forward(self, y, par, freqs):
        """forward pass for training"""
        batch_size = y.size(0) # set the batch size
        # encode data into latent space
        mu_r, log_var_r = self.encode_r(y, freqs) # encode r1(z|y)
        mu_q, log_var_q = self.encode_q(y, par, freqs) # encode q(z|x, y)
        
        # sample z from gaussian with mean and variance from q(z|x, y)
        z_sample = self.gauss_sample(mu_q, log_var_q, batch_size, self.latent_dim)
        #z_sample = self.lorentz_sample(mu_q, log_var_q)[0]
        # get the mean and variance in parameter space from decoder
        if self.dist_type == "studentT":
            mu_par, log_var_par, weight_par = self.decode(z_sample,y, freqs) # decode r2(x|z, y)                                                                              
            return mu_par, log_var_par, weight_par, mu_q, log_var_q, mu_r, log_var_r
        elif self.dist_type == "gaussian":
            mu_par, log_var_par = self.decode(z_sample,y, freqs) # decode r2(x|z, y)                                                                              
            return mu_par, log_var_par, mu_q, log_var_q, mu_r, log_var_r

    def compute_loss(self, y, par, freqs, ramp):
        """
        Comput the loss function given input data 
        """
        mu_r, log_var_r = self.encode_r(y, freqs) # encode r1(z|y)     
        mu_q, log_var_q = self.encode_q(y, par, freqs) # encode q(z|x, y)  

        z_sample = self.gauss_sample(mu_q, log_var_q, mu_q.size(0), mu_q.size(1))

        mu_par, log_var_par = self.decode(z_sample,y, freqs) # decode r2(x|z, y)

        kl_loss = torch.mean(self.KL_gauss(mu_r, log_var_r, mu_q, log_var_q))
        
        gauss_loss = self.log_likelihood_trunc_gauss(par[:,:4], mu_par[:,:4], log_var_par, ramp)

        cat_loss = self.log_likelihood_cat(par[:,4:], mu_par[:,4:])

        recon_loss = -1.0*torch.mean(torch.sum(torch.cat([gauss_loss, cat_loss], axis = 1), axis = 1))
        
        return recon_loss, kl_loss

        
    
    def draw_samples(self, y, mu_r, log_var_r, num_samples, latent_dim, par_dim, return_latent = False, freqs = None):
        """ Draw samples from network for testing"""

        z_sample = self.gauss_sample(mu_r, log_var_r, num_samples, latent_dim)

        # input the latent space samples into decoder r2(x|z, y)  
        #ys = y.repeat(1,num_samples).view(-1, y.size(0)) # repeat data so same size as the z samples
        ys = y.repeat(num_samples,1,1).view(-1, y.size(0), y.size(1)) # repeat data so same size as the z samples
        freqs = freqs.repeat(num_samples).view(-1) # repeat data so same size as the z samples

        # sample parameter space from returned mean and variance 
        mu_par, log_var_par = self.decode(z_sample,ys, freqs) # decode r2(x|z, y) from z        
        samp = self.trunc_gauss_sample(mu_par[:,:4], log_var_par[:,:4])
        
        if np.any(samp[:, :3].cpu().numpy() > 1) or np.any(samp.cpu().numpy()[:,:3] < 0):
            print("samples outside range")
            g1ind = np.where(samp[:,:3].cpu().numpy() > 1)
            l0ind = np.where(samp[:,:3].cpu().numpy() < 0)
            print(samp[g1ind], mu_par[g1ind], log_var_par[g1ind])
            print(samp[l0ind], mu_par[l0ind], log_var_par[l0ind])
            sys.exit()
        # draw only one realisation for the tracks
        track_samp = self.cat_samp(mu_par[:,4:])

        if return_latent:
            return samp.cpu().numpy(), z_sample.cpu().numpy(), track_samp.cpu().numpy()
        else:
            return samp.cpu().numpy(), None, track_samp.cpu().numpy()
    
    def test_latent(self, y, freqs, par, num_samples):
        """generating samples when testing the network, returns latent samples as well (used during training to get latent samples)"""
        num_data = y.size(0)                                                                                                                                                     
        x_samples = []
        track_samples = []
        # encode the data into latent space with r1(z,y)          
        mu_r, log_var_r = self.encode_r(y, freqs) # encode r1(z|y) 
        mu_q, log_var_q = self.encode_q(y,par, freqs) # encode q(z|y) 
        # get the latent space samples
        zr_samples = []
        zq_samples = []
        for i in range(num_data):
            # sample from both r and q networks
            zr_sample = self.gauss_sample(mu_r[i], log_var_r[i], num_samples, self.latent_dim)
            zq_sample = self.gauss_sample(mu_q[i], log_var_q[i], num_samples, self.latent_dim)
            zr_samples.append(zr_sample.cpu().numpy())
            zq_samples.append(zq_sample.cpu().numpy())
            # input the latent space samples into decoder r2(x|z, y)  
            ys = y[i].repeat(num_samples,1,1).view(-1, y.size(1), y.size(2)) # repeat data so same size as the z samples
            freqss = freqs[i].repeat(num_samples).view(-1) # repeat data so same size as the z samples

            mu_par, log_var_par = self.decode(zr_sample,ys, freqss) # decode r2(x|z, y) from z        
            samp = self.trunc_gauss_sample(mu_par[:,:4], log_var_par[:,:4])
            track_samp = self.cat_samp(mu_par[:,4:])

            # add samples to list    
            x_samples.append(samp.cpu().numpy())
            track_samples.append(track_samp.cpu().numpy())
        return np.array(x_samples),np.array(zr_samples),np.array(zq_samples), track_samples
    
    
    def test(self, y, freqs, num_samples, transform_func=None, return_latent = False, par = None):
        """generating samples when testing the network 
        args
        --------
        model : pytorch model
            the input model to test
        y: Tensor
            Tensor of all observation data to generate samples from 
        num_samples: int
            number of samples to draw
        transform_func: function (optional)
            function which transforms the parameters into real parameter space
        return_latent: bool
            if true returns the samples in the latent space as well as output
        par: list (optional)
            parameter for each injection, used if returning the latent space samples (return_latent=True)
        """
        num_data = y.size(0)                                                                                                                                                     
        transformed_samples = []
        net_samples = []
        track_samples = []
        if return_latent:
            z_samples = []
            q_samples = []
        # encode the data into latent space with r1(z,y)          
        mu_r, log_var_r = self.encode_r(y, freqs) # encode r1(z|y) 
        if return_latent:
            mu_q, log_var_q = self.encode_q(y,par, freqs) # encode q(z|y) 
        # get the latent space samples for each input
        for i in range(num_data):
            print("index: {}".format(i))
            # generate initial samples
            t_net_samples, t_znet_samples, t_track_samples = self.draw_samples(y[i], mu_r[i], log_var_r[i], num_samples, self.latent_dim, self.par_dim, return_latent = return_latent, freqs=freqs[i])
            if return_latent:
                q_samples.append(self.gauss_sample(mu_q[i], log_var_q[i], num_samples, self.latent_dim).cpu().numpy())
            if transform_func is None:
                # if nans in samples then keep drawing samples until there are no Nans (for whan samples are outside prior)
                if np.any(np.isnan(t_net_samples)):
                    num_nans = np.inf
                    stime = time.time()
                    while num_nans > 0:
                        nan_locations = np.where(np.any(np.isnan(t_net_samples), axis=1))
                        num_nans = len(nan_locations[0])
                        if num_nans == 0: break
                        temp_new_net_samp, temp_new_z_sample, temp_track_samples = self.draw_samples(y[i], mu_r[i], log_var_r[i], num_nans, self.latent_dim, self.par_dim, return_latent = return_latent, freqs = freqs[i])
                        t_net_samples[nan_locations] = temp_new_net_samp
                        t_track_samples[nan_locations] = temp_track_samples
                        if return_latent:
                            t_znet_samples[nan_locations] = temp_new_z_sample

                        etime = time.time()
                        # if it still nans after 1 min cancel
                        if etime - stime > 0.5*60:
                            print("Failed to find samples within 3 mins")
                            num_nans = 0
                            break

                transformed_samples.append(t_net_samples)
                net_samples.append(t_net_samples)
                track_samples.append(t_track_samples)
                if return_latent:
                    z_samples.append(t_znet_samples)
                
            else:
                # transform all samples to new parameter space
                new_samples = transform_func(t_net_samples, i)
                # if transformed samples are outside prior (nan) then redraw nans until all real values
                if np.any(np.isnan(new_samples)):
                    stime = time.time()
                    num_nans = np.inf
                    while num_nans > 0:
                        nan_locations = np.where(np.any(np.isnan(new_samples), axis=1))
                        num_nans = len(nan_locations[0])
                        if num_nans == 0: break
                        #redraw samples at nan locations
                        temp_new_net_samples, temp_new_z_samples, temp_track_samples = self.draw_samples(y[i], mu_r[i], log_var_r[i], num_nans, self.latent_dim, self.par_dim, return_latent = return_latent, freqs = freqs[i])
                        transformed_newsamp = transform_func(temp_new_net_samples, i)
                        new_samples[nan_locations] = transformed_newsamp
                        t_net_samples[nan_locations] = temp_new_net_samples
                        t_track_samples[nan_locations] = temp_track_samples
                        if return_latent:
                            t_znet_samples[nan_locations] = temp_new_z_samples
                        etime = time.time()
                        # if it still nans after 1 min cancel
                        if etime - stime > 0.5*60:
                            print("Failed to find samples within 30s")
                            num_nans = 0
                            break
                    

                transformed_samples.append(new_samples)
                net_samples.append(t_net_samples)
                track_samples.append(t_track_samples)
                if return_latent:
                    z_samples.append(t_znet_samples)
        
        if return_latent:
            return np.array(transformed_samples), np.array(net_samples), np.array(z_samples), np.array(q_samples), np.array(track_samples)
        else:
            return np.array(transformed_samples), np.array(net_samples), np.array(track_samples)

