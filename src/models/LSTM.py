import base
import tflearn
import tensorflow as tf
import numpy


class LSTM(base.Base):

    def __init__(self, problem_type='multiclass', num_classes=0):

        super().__init__(problem_type, num_classes)
        self.model_type = 'LSTM'

    def mod_input(self, to_np=True):

        if to_np:
            self.x_train = self.x_train.as_matrix()
            self.x_test = self.x_test.as_matrix()
            self.y_train = self.y_train['target'].values
            self.y_test = self.y_test['target'].values
            self.x_tournament = self.x_tournament.drop(['id'], 1).as_matrix()

        self.x_train = numpy.reshape(self.x_train, (self.x_train.shape[0], 1, self.x_train.shape[1]))
        self.x_test = numpy.reshape(self.x_test, (self.x_test.shape[0], 1, self.x_test.shape[1]))
        self.x_tournament = numpy.reshape(self.x_tournament, (self.x_tournament.shape[0], 1, self.x_tournament.shape[1]))

        self.y_train = numpy.reshape(self.y_train, (self.y_train.shape[0], 1))
        self.y_test = numpy.reshape(self.y_test, (self.y_test.shape[0], 1))


    def model(self, layer_size=32, tensorboard_verbose=3, learning_rate=0.001):

        tf.reset_default_graph()
        input_shape = [None, 1, self.x_train.shape[2]]
        net = tflearn.input_data(shape=input_shape)
        net = tflearn.lstm(net, n_units=layer_size, return_seq=True)
        net = tflearn.fully_connected(net, 300, activation='prelu')
        net = tflearn.fully_connected(net, 1, activation='sigmoid')
        with tf.name_scope("TargetsData"):  # placeholder for target variable (i.e. trainY input)
            targetY = tf.placeholder(shape=[None, 1], dtype=tf.float32, name="Y")

        network = tflearn.regression(net,
                                     placeholder=targetY,
                                     optimizer=self.optimizer(learning_rate),
                                     learning_rate=learning_rate,
                                     loss=tflearn.mean_square(net, targetY),
                                     metric=self.accuracy(net, targetY))

        model = tflearn.DNN(network, tensorboard_verbose=tensorboard_verbose)

        self.populate_params(['model_type', 'layer_size', 'tensorboard_verbose','learning_rate'],
                             [self.model_type, layer_size, tensorboard_verbose, learning_rate])

        return model

if __name__ == '__main__':

    """
    LSTM_MODEL = LSTM(problem_type='regression')
    LSTM_MODEL.load_data()
    LSTM_MODEL.mod_input(to_np=True)
    my_model = LSTM_MODEL.model(layer_size=25,
                                tensorboard_verbose=1,
                                learning_rate=0.00001)

    trained_model = LSTM_MODEL.train(my_model,
                                     num_epochs=50,
                                     batch_size=80,
                                     validation_set=(LSTM_MODEL.x_test, LSTM_MODEL.y_test))

    df, r = LSTM_MODEL.predict(trained_model)

    """

