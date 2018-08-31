import tensorflow as tf

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')
    
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1])
    
#return part of values of normal distribution
def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return initial

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return initial
  
class DeepQNetwork:
    def __init__(self):
        
    def _build_net(self):
        self.s = tf.placeholder(tf.float32, [None, 32*32*4],name='s')
        
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')
        
        with tf.variable_scope('eval_net'):
            c_names = ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            
            # Hidden layer 1 conv and pooling : [32x32]x4 --> [16x16]x32
            with tf.variable_scope('l1'):
                W1_conv1 = tf.get_variable('w1', initializer=weight_variable([5,5,4,32]), collections=c_names)
                b_conv1 = tf.get_variable('b1', initializer=bias_variable([32]), collections=c_names)
                l1_s = tf.reshape(self.s, [-1,32,32,4])
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
            
            with tf.variable_scope('output'):
                
            
            
    