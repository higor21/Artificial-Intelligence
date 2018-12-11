# import packages
# matplotlib inline
import pandas as pd
import numpy as np
from scipy import stats
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, precision_recall_curve
from sklearn.metrics import recall_score, classification_report, auc, roc_curve
from sklearn.metrics import precision_recall_fscore_support, f1_score
from sklearn.preprocessing import StandardScaler
from pylab import rcParams
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers

#set random seed and percentage of test data
RANDOM_SEED = 314 #used to help randomly select the data points
TEST_PCT = 0.2 # 20% of the data

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

#set up graphic style in this case I am using the color scheme from xkcd.com
rcParams['figure.figsize'] = 14, 8.7 # Golden Mean
LABELS = ["Normal","Fraude"]
col_list = ["cerulean","scarlet"]# https://xkcd.com/color/rgb/
# sns.set(style='white', font_scale=1.75, palette=sns.xkcd_palette(col_list))

df = pd.read_csv("creditcard.csv")
df.head(n=5)
count_classes = pd.value_counts(df['Class'], sort = True)
count_classes.plot(kind = 'bar', rot=0)
plt.xticks(range(2), LABELS)
plt.title("Frequência por número de observação")
plt.xlabel("Classe")
plt.ylabel("Número de observações");
plt.show()

normal_df = df[df.Class == 0] #save normal_df observations into a separate df
fraud_df = df[df.Class == 1] #do the same for frauds

normal_df.Amount.describe()
fraud_df.Amount.describe()

bins = np.linspace(200, 2500, 100)
plt.hist(normal_df.Amount, bins, alpha=1, normed=True, label='Normal')
plt.hist(fraud_df.Amount, bins, alpha=0.6, normed=True, label='Fraude')
plt.legend(loc='upper right')
plt.title("Quantia por porcentagem de transações (transações \$200+)")
plt.xlabel("Quantia da transação (USD)")
plt.ylabel("Porcentagem de transações(%)");
plt.show()

bins = np.linspace(0, 48, 48) #48 hours
plt.hist((normal_df.Time/(60*60)), bins, alpha=1, normed=True, label='Normal')
plt.hist((fraud_df.Time/(60*60)), bins, alpha=0.6, normed=True, label='Fraude')
plt.legend(loc='upper right')
plt.title("Porcentagem de transações por hora")
plt.xlabel("Tempo de transação medido a partir da primeira transação do dataset (horas)")
plt.ylabel("Porcentagem de transações (%)");
#plt.hist((df.Time/(60*60)),bins)
plt.show()

plt.scatter((normal_df.Time/(60*60)), normal_df.Amount, alpha=0.6, label='Normal')
plt.scatter((fraud_df.Time/(60*60)), fraud_df.Amount, alpha=0.9, label='Fraude')
plt.title("Quantidade de transação por hora")
plt.xlabel("Tempo de transação medido a partir da primeira transação do dataset (horas)")
plt.ylabel('Qauntia (USD)')
plt.legend(loc='upper right')
plt.show()


#normalização e dimensionamento dos dados devido as diferentes magnitudes - o maior valor de magnitude irá
#"passar por cima" (quantia) do valor de menor magnitude (tempo) - PCA já está na forma normal
df_norm = df
df_norm['Time'] = StandardScaler().fit_transform(df_norm['Time'].values.reshape(-1, 1))
df_norm['Amount'] = StandardScaler().fit_transform(df_norm['Amount'].values.reshape(-1, 1))

# divisão do conjunto de treinamento e de teste
train_x, test_x = train_test_split(df_norm, test_size=TEST_PCT, random_state=RANDOM_SEED)
train_x = train_x[train_x.Class == 0] #where normal transactions
train_x = train_x.drop(['Class'], axis=1) #drop the class column


test_y = test_x['Class'] #save the class column for the test set
test_x = test_x.drop(['Class'], axis=1) #drop the class column

train_x = train_x.values #transform to ndarray
test_x = test_x.values

#criação do modelo do encoder/decoder - definição dos parâmetros da rede
nb_epoch = 20
batch_size = 128
input_dim = train_x.shape[1] #num of columns, 30
encoding_dim = 14
hidden_dim = int(encoding_dim / 2) #i.e. 7
learning_rate = 1e-7

input_layer = Input(shape=(input_dim, ))
encoder = Dense(encoding_dim, activation="tanh", activity_regularizer=regularizers.l1(learning_rate))(input_layer)
encoder = Dense(hidden_dim, activation="relu")(encoder)
#encoder = Dense(3, activation="relu")(encoder)

decoder = Dense(hidden_dim, activation='tanh')(encoder)
#decoder = Dense(encoding_dim, activation='relu')(encoder)
decoder = Dense(input_dim, activation='relu')(decoder)

autoencoder = Model(inputs=input_layer, outputs=decoder)

# Treinamento do modelo e criação do log
autoencoder.compile(metrics=['accuracy'],
                    loss='mean_squared_error',
                    optimizer='adam')

cp = ModelCheckpoint(filepath="autoencoder_fraud.h5",
                               save_best_only=True,
                               verbose=0)

tb = TensorBoard(log_dir='./logs',
                histogram_freq=0,
                write_graph=True,
                write_images=True)

history = autoencoder.fit(train_x, train_x,
                    epochs=nb_epoch,
                    batch_size=batch_size,
                    shuffle=True,
                    validation_data=(test_x, test_x),
                    verbose=1,
                    callbacks=[cp, tb]).history

autoencoder = load_model('autoencoder_fraud.h5')


plt.plot(history['loss'], linewidth=2, label='Train')
plt.plot(history['val_loss'], linewidth=2, label='Test')
plt.legend(loc='upper right')
plt.title('Perda do modelo')
plt.ylabel('Perda')
plt.xlabel('Época')
#plt.ylim(ymin=0.70,ymax=1)
plt.show()

test_x_predictions = autoencoder.predict(test_x)
mse = np.mean(np.power(test_x - test_x_predictions, 2), axis=1)
error_df = pd.DataFrame({'Erro_de_reconstrucao': mse,
                        'Classe_verdadeira': test_y})
error_df.describe()

false_pos_rate, true_pos_rate, thresholds = roc_curve(error_df.True_class, error_df.Reconstruction_error)
roc_auc = auc(false_pos_rate, true_pos_rate,)

plt.plot(false_pos_rate, true_pos_rate, linewidth=5, label='AUC = %0.3f'% roc_auc)
plt.plot([0,1],[0,1], linewidth=5)

plt.xlim([-0.01, 1])
plt.ylim([0, 1.01])
plt.legend(loc='lower right')
plt.title('Curva ROC')
plt.ylabel('Taxa de Positivos Verdadeiros')
plt.xlabel('Taxa de Positivos Falsos')
plt.show()

precision_rt, recall_rt, threshold_rt = precision_recall_curve(error_df.True_class, error_df.Reconstruction_error)
plt.plot(recall_rt, precision_rt, linewidth=5, label='Precision-Recall curve')
plt.title('Recall vs Precision')
plt.xlabel('Recall')
plt.ylabel('Precisão')
plt.show()

plt.plot(threshold_rt, precision_rt[1:], label="Precision",linewidth=5)
plt.plot(threshold_rt, recall_rt[1:], label="Recall",linewidth=5)
plt.title('Precisão e recall para valores limiares difrentes')
plt.xlabel('Limiar')
plt.ylabel('Precisão/Recall')
plt.legend()
plt.show()

threshold_fixed = 5
groups = error_df.groupby('True_class')
fig, ax = plt.subplots()

for name, group in groups:
    ax.plot(group.index, group.Reconstruction_error, marker='o', ms=3.5, linestyle='',
            label= "Fraude" if name == 1 else "Normal")
ax.hlines(threshold_fixed, ax.get_xlim()[0], ax.get_xlim()[1], colors="r", zorder=100, label='Limiar')
ax.legend()
plt.title("Erro de reconstrução para diferentes classes")
plt.ylabel("Erro de reconstrução")
plt.xlabel("Data point index")
plt.show();

pred_y = [1 if e > threshold_fixed else 0 for e in error_df.Reconstruction_error.values]
conf_matrix = confusion_matrix(error_df.True_class, pred_y)

plt.figure(figsize=(12, 12))
sns.heatmap(conf_matrix, xticklabels=LABELS, yticklabels=LABELS, annot=True, fmt="d");
plt.title("Matriz de confusão")
plt.ylabel('Classe verdadeira')
plt.xlabel('Classe prevista')
plt.show()

