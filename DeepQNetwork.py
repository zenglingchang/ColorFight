import os
import settings
import numpy as np
import tensorflow as tf

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')
    
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
    
#return part of values of normal distribution
def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return initial

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return initial
  
class DeepQNetwork:
    def __init__(self):
        self.n_actions = settings.n_actions
        self.gamma = settings.reward_decay
        self.lr = settings.learning_rate
        self.epsilon = settings.e_greedy
        self.replace_target_iter = settings.replace_target_iter
        self.memory_size = settings.memory_size
        self.batch_size = settings.batch_size
        self.learn_step_counter = 0
        self.memory_count = 0
        
        # Init memory
        self.memory = np.zeros((self.memory_size, 32*32*4*2+2))
        
        # Build NetWrok
        self._build_net()
        
        self.sess = tf.Session()
        
        # tensorboard --logdir=logs
        tf.summary.FileWriter("logs/", self.sess.graph)
        
        # Load Data or init Data:
        if os.path.isfile("my_net/save_net.ckpt"):
            self._load_data()
        else:
            self.sess.run(tf.global_variables_initializer())
            
        # Cost list    
        self.cost_his = []
        
    def _load_data(self):
        Saver = tf.train.Saver()
        Saver.restore(self.sess, "my_net/save_net.ckpt")
    
    def _write_data(self):
        Saver = tf.train.Saver()
        saver.save(self.sess, "my_net/save_net.ckpt")
    
    def _build_net(self):
        #------------------------------Eval NetWork--------------------------------
        self.keep_prob = tf.placeholder(tf.float32)
        self.s = tf.placeholder(tf.float32, [None, 32, 32, 4],name='s')
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')
        
        with tf.variable_scope('eval_net'):
            c_names = ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            
            # Hidden layer 1 conv and pooling : [32x32]x4 --> [16x16]x32
            with tf.variable_scope('l1'):
                W1_conv1 = tf.get_variable('w1', initializer=weight_variable([5,5,4,32]), collections=c_names)
                b_conv1 = tf.get_variable('b1', initializer=bias_variable([32]), collections=c_names)
                h_conv1 = tf.nn.relu(conv2d(self.s, W1_conv1) + b_conv1)
                h_pool1 = max_pool_2x2(h_conv1)
                
            # Hidden layer 2 conv and pooling : [32x32]x32 --> [8x8]x64
            with tf.variable_scope('l2'):
                W2_conv2 = tf.get_variable('w2', initializer=weight_variable([5,5,32,64]), collections=c_names)
                b2_conv2 = tf.get_variable('b2', initializer=bias_variable([64]), collections=c_names)
                h_conv2 = tf.nn.relu(conv2d(h_pool1, W2_conv2) + b2_conv2 )
                h_pool2 = max_pool_2x2(h_conv2)
                
            # Fully connected layer: [8x8]x64 --> 1024
            with tf.variable_scope('l3'):
                W_fc3 = tf.get_variable('w3', initializer=weight_variable([8*8*64, 1024]), collections=c_names)
                b_fc3 = tf.get_variable('b3', initializer=bias_variable([1024]), collections=c_names)
                h_pool2_flat = tf.reshape(h_pool2, [-1,8*8*64])
                h_fc3 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc3) + b_fc3)
            
            # Output layer: [1024] --> [5] action
            with tf.variable_scope('output'):
                h_fc3_drop = tf.nn.dropout(h_fc3, self.keep_prob)
                W_op = tf.get_variable('w_op', initializer=weight_variable([1024,5]), collections=c_names)
                b_op = tf.get_variable('b_op', initializer=bias_variable([5]), collections=c_names)
                self.q_eval = tf.matmul(h_fc3_drop,W_op) + b_op
                
        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
            
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)
        
        #----------------------------------target NetWork---------------------------------
        self._s = tf.placeholder(tf.float32, [None, 32,32,4], name='s_')
        with tf.variable_scope('target_net'):
            c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            
            # Hidden layer 1 conv and pooling : [32x32]x4 --> [16x16]x32
            with tf.variable_scope('l1'):
                W1_conv1 = tf.get_variable('w1', initializer=weight_variable([5,5,4,32]), collections=c_names)
                b_conv1 = tf.get_variable('b1', initializer=bias_variable([32]), collections=c_names)
                h_conv1 = tf.nn.relu(conv2d(self._s, W1_conv1) + b_conv1)
                h_pool1 = max_pool_2x2(h_conv1)
                
            # Hidden layer 2 conv and pooling : [32x32]x32 --> [8x8]x64
            with tf.variable_scope('l2'):
                W2_conv2 = tf.get_variable('w2', initializer=weight_variable([5,5,32,64]), collections=c_names)
                b2_conv2 = tf.get_variable('b2', initializer=bias_variable([64]), collections=c_names)
                h_conv2 = tf.nn.relu(conv2d(h_pool1, W2_conv2) + b2_conv2 )
                h_pool2 = max_pool_2x2(h_conv2)
                
            # Fully connected layer: [8x8]x64 --> 1024
            with tf.variable_scope('l3'):
                W_fc3 = tf.get_variable('w3', initializer=weight_variable([8*8*64, 1024]), collections=c_names)
                b_fc3 = tf.get_variable('b3', initializer=bias_variable([1024]), collections=c_names)
                h_pool2_flat = tf.reshape(h_pool2, [-1,8*8*64])
                h_fc3 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc3) + b_fc3)
            
            # Output layer: [1024] --> [5] action
            with tf.variable_scope('output'):
                h_fc3_drop = tf.nn.dropout(h_fc3, self.keep_prob)
                W_op = tf.get_variable('w_op', initializer=weight_variable([1024,5]), collections=c_names)
                b_op = tf.get_variable('b_op', initializer=bias_variable([5]), collections=c_names)
                self.q_next = tf.matmul(h_fc3_drop,W_op) + b_op
                
    def store_transition(self, s, a, r, s_):
        s = np.array(s)
        s_ = np.array(s_)
        s = s.reshape((4096))
        s_ = s.reshape((4096))
        
        # Record
        transition = np.hstack((s, [a,r], s_))

        # Write to memory
        index = self.memory_count % self.memory_size
        self.memory[index, :] = transition
        
        self.memory_count += 1
        
    def Choose_action(self, observation):
        observation = np.array(observation)
        observation = observation[np.newaxis, :]
        if np.random.uniform() < self.epsilon:
            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: observation,
                                                                    self.keep_prob: 1.0})
            action = np.argmax(actions_value)
        else:
            action = np.random.randint(0, self.n_actions)
        return action
        
    def learn(self):
        if self.learn_step_counter % self.replace_target_iter == 0:
            
            
                
if __name__ == '__main__':
    DQN = DeepQNetwork()