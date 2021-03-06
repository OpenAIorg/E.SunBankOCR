import tensorflow as tf
from .residual_block import make_basic_block_layer, make_bottleneck_layer

#將fc修改成fc1,fc2也就是加了一層feedforward
class ResNetTypeI(tf.keras.Model):
    def __init__(self, layer_params, config):
        super(ResNetTypeI, self).__init__()

        self.conv1 = tf.keras.layers.Conv2D(filters=64,
                                            kernel_size=(7, 7),
                                            strides=2,
                                            padding="same")
        self.bn1 = tf.keras.layers.BatchNormalization()
        self.pool1 = tf.keras.layers.MaxPool2D(pool_size=(3, 3),
                                               strides=2,
                                               padding="same")

        self.layer1 = make_basic_block_layer(filter_num=64,
                                             blocks=layer_params[0])
        self.layer2 = make_basic_block_layer(filter_num=128,
                                             blocks=layer_params[1],
                                             stride=2)
        self.layer3 = make_basic_block_layer(filter_num=256,
                                             blocks=layer_params[2],
                                             stride=2)
        self.layer4 = make_basic_block_layer(filter_num=512,
                                             blocks=layer_params[3],
                                             stride=2)

        self.avgpool = tf.keras.layers.GlobalAveragePooling2D()
        # self.fc1     = tf.keras.layers.Dense(units=config.MODEL.BACKBONE_OUTPUT_SIZE, activation=tf.keras.activations.relu)
        # self.fc1     = tf.keras.layers.Dense(units=config.MODEL.NUM_CLASSES, activation=tf.keras.activations.relu)
        # self.fc2     = tf.keras.layers.Dense(units=config.MODEL.NUM_CLASSES, activation=tf.keras.activations.softmax)

    def call(self, inputs, training=None, mask=None):
        x = self.conv1(inputs)
        x = self.bn1(x, training=training)
        x = tf.nn.relu(x)
        x = self.pool1(x)
        x = self.layer1(x, training=training)
        x = self.layer2(x, training=training)
        x = self.layer3(x, training=training)
        x = self.layer4(x, training=training)
        print("look shape", x.shape)
        output = self.avgpool(x)
        print("look shape", output.shape)
        # output = self.fc1(x)
        print("look shape", output.shape)
        # output = self.fc2(output)


        return output


class ResNetTypeII(tf.keras.Model):
    def __init__(self, layer_params, config):
        super(ResNetTypeII, self).__init__()
        self.conv1 = tf.keras.layers.Conv2D(filters=64,
                                            kernel_size=(7, 7),
                                            strides=2,
                                            padding="same")
        self.bn1 = tf.keras.layers.BatchNormalization()
        self.pool1 = tf.keras.layers.MaxPool2D(pool_size=(3, 3),
                                               strides=2,
                                               padding="same")

        self.layer1 = make_bottleneck_layer(filter_num=64,
                                            blocks=layer_params[0])
        self.layer2 = make_bottleneck_layer(filter_num=128,
                                            blocks=layer_params[1],
                                            stride=2)
        self.layer3 = make_bottleneck_layer(filter_num=256,
                                            blocks=layer_params[2],
                                            stride=2)
        self.layer4 = make_bottleneck_layer(filter_num=512,
                                            blocks=layer_params[3],
                                            stride=2)

        self.avgpool = tf.keras.layers.GlobalAveragePooling2D()
        # self.fc1     = tf.keras.layers.Dense(units=config.MODEL.BACKBONE_OUTPUT_SIZE, activation=tf.keras.activations.relu)
        # self.fc2     = tf.keras.layers.Dense(units=config.MODEL.NUM_CLASSES, activation=tf.keras.activations.softmax)

    def call(self, inputs, training=None, mask=None):
        x = self.conv1(inputs)
        x = self.bn1(x, training=training)
        x = tf.nn.relu(x)
        x = self.pool1(x)
        x = self.layer1(x, training=training)
        x = self.layer2(x, training=training)
        x = self.layer3(x, training=training)
        x = self.layer4(x, training=training)
        output = self.avgpool(x)
        # output = self.fc1(output)
        # output = self.fc2(output)
        return output


def resnet_18(config):
    return ResNetTypeI(layer_params=[2, 2, 2, 2], config=config)


def resnet_34(config):
    return ResNetTypeI(layer_params=[3, 4, 6, 3], config=config)


def resnet_50(config):
    return ResNetTypeII(layer_params=[3, 4, 6, 3], config=config)


def resnet_101(config):
    return ResNetTypeII(layer_params=[3, 4, 23, 3], config=config)


def resnet_152(config):
    return ResNetTypeII(layer_params=[3, 8, 36, 3], config=config)
