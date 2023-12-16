import os
import pandas as pd
import keras_tuner
from keras_tuner.tuners import BayesianOptimization
import tensorflow as tf

from util import utils
from metrics import evaluate
from pathlib import Path
from visualization import graphs


class DeepRegressor:
    def __init__(self,
                 dataset_dict:dict,
                 config:dict,
                 models_dir:str,
                 parameters_dict:dict,
                 scaler,
                 df_test):

        self.dataset_dict=dataset_dict
        self.config=config
        self.models_dir=models_dir
        self.parameters_dict=parameters_dict
        self.scaler=scaler
        self.df_test=df_test

        self.problem_type='anomaly'
        self.cwd = Path.cwd()
        self.X_train, self.y_train = dataset_dict['df_train'][0], dataset_dict['df_train'][1]
        self.X_test, self.y_test = dataset_dict['df_test'][0],dataset_dict['df_test'][1]
        model=self.get_model_class(self.problem_type,config.module_name,config.network_name)
        self.network=model(self.X_train.shape[1:],1)


    def define_callback(self,early_stop=False,reduceLR=False,tensorboard=False)->list:
        callback_list=[]
        if early_stop:
            early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=6)
            callback_list.append(early_stop)
        if reduceLR:
            #Exponential Decay also is another option
            ReduceLROnPlateau = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3,min_lr=1e-8)
            callback_list.append(ReduceLROnPlateau)

        if tensorboard:
            #to run cd to models directory and run this command while in the models directory:
            #tensorboard --logdir tensorboard/
            from keras.callbacks import TensorBoard
            tensorboard_dir = os.path.join(self.models_dir, 'tensorboard')
            tensorboard_callback = TensorBoard(log_dir=tensorboard_dir, histogram_freq=1)  # profile_batch='500,520'
            callback_list.append(tensorboard_callback)

        return callback_list

    def search_hyperparam(self):

        hypermodel=self.network
        callbacks=self.define_callback(early_stop=True,reduceLR=True)
        tuner=BayesianOptimization(hypermodel,objective=keras_tuner.Objective("val_loss",direction="min")
                                   ,seed=1,max_trials=self.config.max_trials, directory=os.path.normpath(self.cwd),project_name='RS',overwrite=True)

        tuner.search_space_summary()
        tuner.search(self.X_train,self.y_train,validation_split=self.parameters_dict["val_ratio"],callbacks=callbacks,batch_size=self.parameters_dict['batch_size'],
                     verbose=1,epochs=self.config.epochs,use_multiprocessing=True)
        return tuner


    def fit(self):
        tuner=self.search_hyperparam()
        best_hps=tuner.get_best_hyperparameters(self.config.max_trials)

        return tuner, best_hps

    def save_2(self, tuner, best_hps):
        callbacks = self.define_callback(early_stop=True, reduceLR=True, tensorboard=True)

        for index, trial in enumerate(best_hps):
            model=tuner.hypermodel.build(trial)
            history=model.fit(self.X_train,self.y_train,validation_split=self.parameters_dict["val_ratio"],epochs=self.config.epochs,callbacks=callbacks,
                              batch_size=self.parameters_dict['batch_size'],verbose=1,use_multiprocessing=True)

            hp_config = {}
            hp_config.update(trial.values)
            lr = trial["learning_rate"]
            record_name = f"{self.parameters_dict['window_size']}ws_{self.parameters_dict['stride_size']}ss_" \
                          f"{self.parameters_dict['scaler_type']}_{self.parameters_dict['val_ratio']}vr_{index}"

            # model_path=os.path.join(self.models_dir,record_name)
            # utils.make_dir(model_path)
            model_path= self.models_dir / record_name
            model_path.mkdir(exist_ok=True)
            model.save(model_path)

            train_mae_loss, test_mae_loss = evaluate.model_test(model, self.X_train, self.X_test)

            graphs.plot_distplot(train_mae_loss, model_path)
            graphs.plot_anomalies(self.df_test,
                                  self.parameters_dict['window_size'],
                                  test_mae_loss,
                                  self.config.THRESHOLD,
                                  self.scaler,
                                  model_path)
            graphs.train_evaluation_graphs(history, model_path, index)

    def save(self, trial, model,index,history):
        import mlflow
        hp_config = {}
        hp_config.update(trial.values)
        lr=trial["learning_rate"]

        no_of_model=f"{self.parameters_dict['window_size']}ws_{self.parameters_dict['stride_size']}ss_" \
                    f"{self.parameters_dict['scaler_type']}_{self.parameters_dict['val_ratio']}vr_{index}"
        #no_of_model=f"{self.observation_name}_lr{str(lr)[:8]}_{self.start_time[-4:]}_{index}"

        model_path=os.path.join(self.models_dir,no_of_model)
        utils.make_dir(model_path)
        model.save(model_path)
        THRESHOLD = 0.4
        train_mae_loss, test_mae_loss=evaluate.model_test(
                            model=model,
                            dataset_dict=self.dataset_dict)

        graphs.plot_distplot(train_mae_loss,model_path)
        graphs.plot_anomalies(self.df_test,self.parameters_dict['window_size'],test_mae_loss,THRESHOLD,self.scaler,model_path)
        graphs.train_evaluation_graphs(history, model_path, index)



        #metrics={"loss":128,"MAE": 36, "R2": 0.86} #TODO delete after
        # for k2, v2 in hp_config.items():
        #     df_result.loc[:, k2] = [v2]
        #
        # for k3,v3 in self.parameters_dict.items():
        #     df_result.loc[:,k3]=[v3]
        #
        # mlflow.set_experiment(self.observation_name)
        # with mlflow.start_run() as run:
        #     #mlflow.set_tracking_uri("http://localhost:5000")
        #     # mlflow.log_params(df_result)
        #     mlflow.log_params(trial.values)
        #     #signature = infer_signature(self.X_train, y_pred)
        #     mlflow.tensorflow.log_model(model,'model')
        #     #mlflow.log_metrics(metrics.to_dict()) #dict istiyor.
        #     mlflow.log_metric('mae',metrics['MAE'])
        #     mlflow.log_metric('r2',metrics['R2'])
        #     mlflow.log_artifact(model_path + f"/TrueVSpred_{index}.png", "png")
        #     #TODO PATHLID ILE YAPILACAK
        #     #artifact_path=model_path / f"/TrueVSpred_{self.observation_name}_{index}.png"
        #     # artifact_path_2=model_path / f"/R2_{self.observation_name}_{index}.png"
        #     # mlflow.log_artifact(model_path + f"/R2_{self.observation_name}_{index}.png","png")
        # return df_result

    def get_model_class(self,problem_type:str,module_name:str,model_name:str):
        import  importlib

        imported_module=importlib.import_module(f"models.{problem_type}.{module_name}")
        model=getattr(imported_module,model_name)
        return model
