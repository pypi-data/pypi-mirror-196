import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Dropout, Conv2D, MaxPool2D, ZeroPadding2D, Reshape


def create_dnn_model(input_shape, output_shape, layers, activation, dropout=None):

    """
    Build Tensorflow model for DNN

    Parameters
    ----------
    input_shape : tuple or TensorShape
        Shape tuple (not including the batch axis), or TensorShape instance (not including the batch axis).
        Note that window_length should be the first element of its shape.
    output_shape : int
        A shape of final dimension.
    layers : list[int]
        List of the number of nodes in each hidden layer. len(layers) determines the number of hidden layers.
    activation : relevent module or str
        Activation function, such as tf.nn.relu, or string name of built-in activation function, such as "relu".
    dropout : None or float
        Float between 0 and 1. Fraction of the input units to drop. If None, dropout will be skipped.
    """

    initializer = tf.keras.initializers.RandomUniform(minval=-1e-3, maxval=1e-3, seed=1)

    model = Sequential()
    model.add(Flatten(input_shape=input_shape))
    for layer in layers:
        model.add(Dense(layer, kernel_initializer=initializer))
        model.add(Activation(activation))
        if dropout is not None:
            model.add(Dropout(rate=dropout))
    model.add(Dense(output_shape, kernel_initializer=initializer))
    model.add(Activation('linear'))

    return model


def create_cnn_model(input_shape, output_shape,
                     filters_list, kernel_size_list, strides, padding, activation,
                     pool_size, pool_strides, layers, dropout=None):

    """
    Build Tensorflow model for CNN

    Description
        - Overall Architecture
            * part 1 (CNN) : Input -> Reshape -> (ZeroPadding2D + Conv2D + MaxPool2D) * len(kernel_sizes) -> Flatten
            * part 2 (FC) : Flatten -> (Dense + Activation + Dropout) * len(layers) -> Output

    Parameters
    ----------
    input_shape : tuple or TensorShape
        Shape tuple (not including the batch axis), or TensorShape instance (not including the batch axis).
        Note that window_length should be the first element of its shape.
    output_shape : int
        A shape of final dimension.
    filters_list : list[int]
        The dimensionality of the output space (i.e. the number of output filters in the convolution).
    kernel_size_list : list[tuple or int]
        An element of this specifies the height and width of the 2D convolution window (if integer, the window has
        same spatial dimensions). Since each elements mean each layers, len(kernel_sizes) determines the number of
        convolutional layers.
    strides : int or tuple
        An integer or tuple/list of 2 integers, specifying the strides of the convolution along the height and
        width. Can be a single integer to specify the same value for all spatial dimensions. Specifying any stride
        value != 1 is incompatible with specifying any dilation_rate value != 1.
    padding : int, tuple[int], or tuple[tuple[int], tuple[int]]
        int -> the same symmetric padding is applied to height and width.
        tuple of 2 ints -> interpreted as two different symmetric padding values for height and width:
            (symmetric_height_pad, symmetric_width_pad).
        tuple of 2 tuples of 2 ints -> interpreted as ((top_pad, bottom_pad), (left_pad, right_pad))
    activation : relevent module or str
        Activation function, such as tf.nn.relu, or string name of built-in activation function, such as "relu".
    pool_size : int or tuple[int]
        Window size over which to take the maximum. If only one integer is specified, the same window length will be
        used for both dimensions.
    pool_strides : int, tuple[int], or None
        Strides values. Specifies how far the pooling window moves for each pooling step. If None, it will default
        to pool_size.
    layers : list[int]
        List of the number of nodes in each hidden layer. len(layers) determines the number of hidden layers.
    dropout : None or float
        Float between 0 and 1. Fraction of the input units to drop. If None, dropout will be skipped.
    """

    # Default kwargs
    initializer = tf.keras.initializers.RandomUniform(minval=-1e-3, maxval=1e-3, seed=1)
    conv_kwargs = {'strides': strides, 'activation': activation, 'kernel_initializer': initializer}
    pool_kwargs = {'pool_size': pool_size, 'strides': pool_strides, 'padding': 'valid'}

    # Convolutional Network
    model = Sequential()
    model.add(Reshape(input_shape=input_shape, target_shape=input_shape[1:]))
    model.add(ZeroPadding2D(padding=padding))
    model.add(Conv2D(kernel_size=kernel_size_list[0], filters=filters_list[0], **conv_kwargs))
    model.add(MaxPool2D(**pool_kwargs))
    for kernel_size, filters in zip(kernel_size_list[1:], filters_list[1:]):
        model.add(ZeroPadding2D(padding=padding))
        model.add(Conv2D(kernel_size=kernel_size, filters=filters, **conv_kwargs))
        model.add(MaxPool2D(**pool_kwargs))

    # Fully-Connected Layers
    model.add(Flatten())
    for layer in layers:
        model.add(Dense(layer, kernel_initializer=initializer))
        model.add(Activation(activation))
        if dropout is not None:
            model.add(Dropout(rate=dropout))
    model.add(Dense(output_shape, kernel_initializer=initializer))
    model.add(Activation('linear'))

    return model
