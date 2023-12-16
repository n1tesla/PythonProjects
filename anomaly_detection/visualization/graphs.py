import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

def plot_distplot(loss,model_path):
    fig=sns.distplot(loss,bins=50,kde=True)
    #fig.savefig(model_path + f"/train_mae_distplot.png", format="png")


def plot_anomalies(df_test,window_size,test_mae_loss,THRESHOLD,scaler,model_path):


    test_score_df = pd.DataFrame(index=df_test[window_size:].index)
    test_score_df['loss'] = test_mae_loss[:-1]
    test_score_df['threshold'] = THRESHOLD
    test_score_df['anomaly'] = test_score_df.loss > test_score_df.threshold
    test_score_df['close'] = df_test[window_size:].close
    anomalies = test_score_df[test_score_df.anomaly == True]

    plt.plot(test_score_df.index, test_score_df.loss, label='loss')
    plt.plot(test_score_df.index, test_score_df.threshold, label='threshold')
    plt.xticks(rotation=25)
    plt.legend();
    arr_test=df_test[window_size:].close.to_numpy()
    arr_test=np.expand_dims(arr_test,axis=1)

    plt.plot(
        df_test[window_size:].index,
        scaler.inverse_transform(arr_test),
        label='close price'
    );
    arr_anomalies=anomalies.close.to_numpy()
    arr_anomalies=np.expand_dims(arr_anomalies,axis=1)
    data=pd.DataFrame({'anomalies_index':anomalies.index,'anomalies':scaler.inverse_transform(arr_anomalies)})
    sns.scatterplot(
        data,
        x='anomalies_index',
        y='anomalies',
        color=sns.color_palette()[3],
        s=52,
        label='anomaly'
    )
    plt.xticks(rotation=25)
    plt.legend();

    plt.title('Anomaly Detection')
    plt.savefig(model_path + f"/anomalies.png", format="png")

    #
    # plot_path_2 = model_path / f"anomalies.png"
    # plt.savefig(plot_path_2)

def plot_result(y_true: np.ndarray, y_pred: np.ndarray, model_path: str, index: int,
                result:pd.DataFrame):

    result_string = ""

    for column_name, value in result.iloc[0].items():
        result_string += f"{column_name} : {value}\n"

    plt.rcParams['figure.figsize'] = 12, 10
    plt.plot(y_pred)
    plt.plot(y_true)
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
    plt.figtext(x=0.1,y=0.94, s=result_string, bbox=bbox,ha='left',va = 'top')
    plt.ylabel('RUL')
    plt.xlabel('samples')
    plt.legend(('Predicted', 'True'), loc='upper right')
    plt.title('COMPARISION OF Real and Predicted values')
    plt.savefig(model_path + f"/TrueVSpred_{index}.png", format="png")
    # plot_dir=plots_path / f"/TrueVSpred_{index}.png"
    # plt.savefig(plots_path, format="png")
    plt.close()


def train_evaluation_graphs(history, model_path: str, index: int):


    fig_acc = plt.figure(figsize=(10, 10))
    plt.plot(history.history['mae'])
    plt.plot(history.history['val_mae'])
    plt.title('model MAE')
    plt.ylabel('MAE')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig(model_path + f"/MAE_{index}.png", format="png")
    plt.close()


    # summarize history for Loss
    fig_acc = plt.figure(figsize=(10, 10))
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig(model_path + f"/Loss_{index}.png", format="png")
    plt.close()


