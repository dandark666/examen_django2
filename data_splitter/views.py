# data_splitter/views.py
import pandas as pd
import numpy as np
import base64
import io
from sklearn.model_selection import train_test_split
from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generate_realistic_data():
    """Genera datos realistas basados en el ejemplo que proporcionaste"""
    np.random.seed(42)
    n_samples = 125973
    
    # Basado en tu dataset real
    protocols = np.random.choice(['tcp', 'udp', 'icmp'], n_samples, p=[0.7, 0.25, 0.05])
    services = np.random.choice(['http', 'private', 'smtp', 'ftp_data', 'domain_u', 'eco_i'], n_samples, 
                               p=[0.3, 0.2, 0.15, 0.1, 0.15, 0.1])
    flags = np.random.choice(['SF', 'S0'], n_samples, p=[0.8, 0.2])
    
    df = pd.DataFrame({
        'duration': np.random.exponential(1, n_samples),
        'protocol_type': protocols,
        'service': services,
        'flag': flags,
        'src_bytes': np.random.lognormal(6, 3, n_samples),
        'dst_bytes': np.random.lognormal(8, 3, n_samples),
        'land': np.zeros(n_samples),
        'wrong_fragment': np.random.exponential(0.1, n_samples),
        'urgent': np.zeros(n_samples),
        'hot': np.random.exponential(0.1, n_samples),
        'dst_host_count': np.random.randint(1, 255, n_samples),
        'dst_host_srv_count': np.random.randint(1, 255, n_samples),
        'dst_host_same_srv_rate': np.random.uniform(0, 1, n_samples),
        'dst_host_diff_srv_rate': np.random.uniform(0, 0.1, n_samples),
        'dst_host_same_src_port_rate': np.random.uniform(0, 1, n_samples),
        'dst_host_srv_diff_host_rate': np.random.uniform(0, 0.1, n_samples),
        'dst_host_serror_rate': np.random.uniform(0, 1, n_samples),
        'dst_host_srv_serror_rate': np.random.uniform(0, 1, n_samples),
        'dst_host_rerror_rate': np.random.uniform(0, 0.1, n_samples),
        'dst_host_srv_rerror_rate': np.random.uniform(0, 0.1, n_samples)
    })
    
    return df

def train_val_test_split(df, rstate=42, shuffle=True, stratify=None):
    """Función de particionado - EXACTAMENTE igual a tu código original"""
    strat = df[stratify] if stratify else None
    train_set, test_set = train_test_split(
        df, test_size=0.4, random_state=rstate, shuffle=shuffle, stratify=strat)
    strat = test_set[stratify] if stratify else None
    val_set, test_set = train_test_split(
        test_set, test_size=0.5, random_state=rstate, shuffle=shuffle, stratify=strat)
    return (train_set, val_set, test_set)

def home(request):
    # Generar datos realistas
    df = generate_realistic_data()
    
    # Realizar particionado
    train_set, val_set, test_set = train_val_test_split(df, stratify='protocol_type')
    
    # Crear las gráficas individuales
    individual_plots = {}
    
    # Gráfica 1: Dataset original - protocol_type
    plt.figure(figsize=(10, 6))
    df["protocol_type"].value_counts().sort_index().plot(kind='bar', color=['skyblue', 'lightcoral', 'lightgreen'])
    plt.title('Dataset Original - protocol_type')
    plt.xlabel('Protocol Type')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    
    buf_original = io.BytesIO()
    plt.savefig(buf_original, format='png', dpi=100)
    buf_original.seek(0)
    individual_plots['original'] = base64.b64encode(buf_original.getvalue()).decode('utf-8')
    plt.close()
    
    # Gráfica 2: Training set - protocol_type
    plt.figure(figsize=(10, 6))
    train_set["protocol_type"].value_counts().sort_index().plot(kind='bar', color=['skyblue', 'lightcoral', 'lightgreen'])
    plt.title('Training Set - protocol_type')
    plt.xlabel('Protocol Type')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    
    buf_train = io.BytesIO()
    plt.savefig(buf_train, format='png', dpi=100)
    buf_train.seek(0)
    individual_plots['train'] = base64.b64encode(buf_train.getvalue()).decode('utf-8')
    plt.close()
    
    # Gráfica 3: Validation set - protocol_type
    plt.figure(figsize=(10, 6))
    val_set["protocol_type"].value_counts().sort_index().plot(kind='bar', color=['skyblue', 'lightcoral', 'lightgreen'])
    plt.title('Validation Set - protocol_type')
    plt.xlabel('Protocol Type')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    
    buf_val = io.BytesIO()
    plt.savefig(buf_val, format='png', dpi=100)
    buf_val.seek(0)
    individual_plots['val'] = base64.b64encode(buf_val.getvalue()).decode('utf-8')
    plt.close()
    
    # Gráfica 4: Test set - protocol_type
    plt.figure(figsize=(10, 6))
    test_set["protocol_type"].value_counts().sort_index().plot(kind='bar', color=['skyblue', 'lightcoral', 'lightgreen'])
    plt.title('Test Set - protocol_type')
    plt.xlabel('Protocol Type')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    
    buf_test = io.BytesIO()
    plt.savefig(buf_test, format='png', dpi=100)
    buf_test.seek(0)
    individual_plots['test'] = base64.b64encode(buf_test.getvalue()).decode('utf-8')
    plt.close()
    
    # Gráfica comparativa (las 4 juntas)
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    df["protocol_type"].value_counts().sort_index().plot(kind='bar', color=['skyblue', 'lightcoral', 'lightgreen'])
    plt.title('Dataset Original')
    plt.ylabel('Frecuencia')
    
    plt.subplot(2, 2, 2)
    train_set["protocol_type"].value_counts().sort_index().plot(kind='bar', color=['skyblue', 'lightcoral', 'lightgreen'])
    plt.title('Training Set')
    plt.ylabel('Frecuencia')
    
    plt.subplot(2, 2, 3)
    val_set["protocol_type"].value_counts().sort_index().plot(kind='bar', color=['skyblue', 'lightcoral', 'lightgreen'])
    plt.title('Validation Set')
    plt.ylabel('Frecuencia')
    
    plt.subplot(2, 2, 4)
    test_set["protocol_type"].value_counts().sort_index().plot(kind='bar', color=['skyblue', 'lightcoral', 'lightgreen'])
    plt.title('Test Set')
    plt.ylabel('Frecuencia')
    
    plt.tight_layout()
    
    buf_comparative = io.BytesIO()
    plt.savefig(buf_comparative, format='png', dpi=100)
    buf_comparative.seek(0)
    plot_url = base64.b64encode(buf_comparative.getvalue()).decode('utf-8')
    plt.close()
    
    # Estadísticas
    stats = {
        'total_samples': len(df),
        'train_samples': len(train_set),
        'val_samples': len(val_set),
        'test_samples': len(test_set),
    }
    
    # Distribuciones
    distributions = {
        'original': df['protocol_type'].value_counts().sort_index().to_dict(),
        'train': train_set['protocol_type'].value_counts().sort_index().to_dict(),
        'val': val_set['protocol_type'].value_counts().sort_index().to_dict(),
        'test': test_set['protocol_type'].value_counts().sort_index().to_dict(),
    }
    
    context = {
        'plot_url': plot_url,
        'individual_plots': individual_plots,
        'stats': stats,
        'distributions': distributions,
    }
    
    return render(request, 'index.html', context)