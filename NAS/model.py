from keras.models import Model
from keras.layers import Input, Dense, Conv2D, GlobalAveragePooling2D,LSTM

def model_fn(actions):

    input_layer=Input(shape=(30,8))
    units_1, units_2, units_3 = actions
    x=LSTM(units=units_1, return_sequences=True)(input_layer) #128
    x=LSTM(units=units_2,return_sequences=True)(x)
    x=LSTM(units=units_3)(x)

    output_layer=Dense(1,activation='linear')(x)
    model=Model(inputs=input_layer,outputs=output_layer)

    # unpack the actions from the list
    # kernel_1, filters_1, kernel_2, filters_2, kernel_3, filters_3, kernel_4, filters_4 = actions
    #
    # ip = Input(shape=(32, 32, 3))
    # x = Conv2D(filters_1, (kernel_1, kernel_1), strides=(2, 2), padding='same', activation='relu')(ip)
    # x = Conv2D(filters_2, (kernel_2, kernel_2), strides=(1, 1), padding='same', activation='relu')(x)
    # x = Conv2D(filters_3, (kernel_3, kernel_3), strides=(2, 2), padding='same', activation='relu')(x)
    # x = Conv2D(filters_4, (kernel_4, kernel_4), strides=(1, 1), padding='same', activation='relu')(x)
    # x = GlobalAveragePooling2D()(x)
    # x = Dense(10, activation='softmax')(x)


    return model


# generic models design
# def model_fn(actions):
#     # unpack the actions from the list
#     kernel_1, filters_1, kernel_2, filters_2, kernel_3, filters_3, kernel_4, filters_4 = actions
#
#     ip = Input(shape=(32, 32, 3))
#     x = Conv2D(filters_1, (kernel_1, kernel_1), strides=(2, 2), padding='same', activation='relu')(ip)
#     x = Conv2D(filters_2, (kernel_2, kernel_2), strides=(1, 1), padding='same', activation='relu')(x)
#     x = Conv2D(filters_3, (kernel_3, kernel_3), strides=(2, 2), padding='same', activation='relu')(x)
#     x = Conv2D(filters_4, (kernel_4, kernel_4), strides=(1, 1), padding='same', activation='relu')(x)
#     x = GlobalAveragePooling2D()(x)
#     x = Dense(10, activation='softmax')(x)
#
#     model = Model(ip, x)
#     return model
