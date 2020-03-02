import torch
import torch.nn as nn
import torch.nn.functional as F

class deepKNet(nn.Module):
    def __init__(self):
        super(deepKNet, self).__init__()
        ## TF settings
        # net = tf.keras.layers.Conv1D(128, 1, activation=tf.nn.relu)(feat)
        # net = tf.keras.layers.Conv1D(256, 3, padding="same", activation=tf.nn.relu)(net)
        # for i in range(0, 5):
        #   intmp = net
        #   net = tf.keras.layers.Conv1D(256, 3, padding="same", dilation_rate=2**i, activation=None)(net)
        #   net = tf.keras.layers.BatchNormalization()(net)
        #   net += intmp # residue connection
        #   net = tf.nn.relu(net)
        #   
        # net = tf.keras.layers.Conv1D(512, 3, padding="same", activation=tf.nn.relu)(net)
        # for i in range(0, 5):
        #   intmp = net
        #   net = tf.keras.layers.Conv1D(512, 3, padding="same", dilation_rate=2**i, activation=None)    (net)
        #   net = tf.keras.layers.BatchNormalization()(net)
        #   net += intmp # residue connection
        #   net = tf.nn.relu(net)
        #
        # net = tf.keras.layers.Conv1D(1024, 3, padding="same", activation=tf.nn.relu)(net)
        # for i in range(0, 5):
        #   intmp = net
        #   net = tf.keras.layers.Conv1D(1024, 3, padding="same", dilation_rate=2**i, activation=None    )(net)
        #   net = tf.keras.layers.BatchNormalization()(net)
        #   net += intmp # residue connection
        #   net = tf.nn.relu(net)
        #
        # net = tf.math.reduce_max(net, axis=1)
        # net = tf.reshape(net, [-1, 1024])
        # net = tf_util.fully_connected(net, 512, bn=False, is_training=is_training,
        #           scope='fc1', bn_decay=bn_decay)
        # net = tf_util.fully_connected(net, 256, bn=False, is_training=is_training,
        #           scope='fc2', bn_decay=bn_decay)
        # net = tf_util.fully_connected(net, 64, bn=False, is_training=is_training,
        #           scope='fc3', bn_decay=bn_decay)
        # y_pred = tf_util.fully_connected(net, 1, activation_fn=None, scope='fc4')


        self.conv1 = torch.nn.Conv1d(97, 64, 1)
        self.conv2 = torch.nn.Conv1d(64, 128, 1)
        self.conv3 = torch.nn.Conv1d(128, 1024, 1)
        self.bn1 = nn.BatchNorm1d(64)
        self.bn2 = nn.BatchNorm1d(128)
        self.bn3 = nn.BatchNorm1d(1024)
        self.fc1 = nn.Linear(1024, 1)

    def forward(self, point_cloud):
        # point_cloud size -- (batch_size, nfeatures, npoints)
        # current settings -- (        16,      3+94,     512)
        out = F.relu(self.bn1(self.conv1(point_cloud)))
        out = F.relu(self.bn2(self.conv2(out)))
        out = F.relu(self.bn3(self.conv3(out)))
        # max pooling
#        out = torch.max(out, dim=2, keepdim=True)[0]
        # mean pooling
        out = torch.mean(out, dim=2)
        # reshape tensor
        out = out.view(-1, 1024)
        out = self.fc1(out)
        return out
 

