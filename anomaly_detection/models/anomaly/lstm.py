
from keras_tuner import HyperModel
from keras.layers import Dense,LSTM, Dropout,Input, RepeatVector,TimeDistributed
from keras.models import Model
from keras.optimizers import RMSprop,Adam


class LSTM_AnomalyNetwork(HyperModel):
    def __init__(self,input_shape:list,nb_output:int):
        self.input_shape=input_shape
        self.nb_output=nb_output

    def build(self,hp):

        input_layer=Input(self.input_shape)
        lstm1=LSTM(units=hp.Choice(f"LSTM_1_units",values=[128,256]))(input_layer) #128
        dropout1=Dropout(rate=hp.Float(f"Dropout_1_rate",min_value=0.2,max_value=0.7))(lstm1)   #0.55
        # lstm2 = LSTM(units=hp.Int(f"LSTM_2_units",min_value=50,max_value=256))(dropout1) #256
        # dropout2=Dropout(rate=hp.Float(f"Dropout_2_rate",min_value=0.2,max_value=0.7))(lstm2)   #031
        repeat_vector=RepeatVector(n=self.input_shape[0])(dropout1)

        lstm3=LSTM(units=hp.Choice(f"LSTM_3_units",values=[128,256]), return_sequences=True)(repeat_vector) #128
        dropout3=Dropout(rate=hp.Float(f"Dropout_3_rate",min_value=0.2,max_value=0.7))(lstm3)   #0.55
        # lstm4 = LSTM(units=hp.Int(f"LSTM_4_units",min_value=50,max_value=256,),return_sequences=True)(dropout3) #256
        # dropout4=Dropout(rate=hp.Float(f"Dropout_4_rate",min_value=0.2,max_value=0.7))(lstm4)   #031

        output_layer=TimeDistributed(Dense(units=1,activation='linear'))(dropout3)
        lr=hp.Float(f"learning_rate",min_value=1e-6,max_value=1e-3)
        model=Model(inputs=input_layer,outputs=output_layer)
        model.compile(loss='mae',optimizer=Adam(learning_rate=lr))
        model.summary()
        return model