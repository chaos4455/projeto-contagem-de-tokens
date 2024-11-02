import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import sqlite3
import os
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy import stats
from wordcloud import WordCloud
import calendar
import plotly.figure_factory as ff

# Criar pasta reports se não existir
if not os.path.exists('reports'):
    os.makedirs('reports')

# Conectar ao banco de dados
conn = sqlite3.connect('vectors_continuo.db')

# Carregar dados - Query atualizada
df = pd.read_sql_query("""
    SELECT 
        word,
        palavra_origem,
        timestamp,
        LENGTH(vector) as vector_size,
        id
    FROM word_vectors
    ORDER BY timestamp
""", conn)

# Converter timestamp para datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hora'] = df['timestamp'].dt.hour
df['data'] = df['timestamp'].dt.date

# Inicializar app Dash
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Análise de Vetores Contínuos", style={'textAlign': 'center'}),
    
    # Grid de gráficos
    html.Div([
        # Primeira linha
        html.Div([
            dcc.Graph(id='palavras-por-hora'),
            dcc.Graph(id='distribuicao-tamanhos'),
        ], style={'display': 'flex'}),
        
        # Segunda linha
        html.Div([
            dcc.Graph(id='origem-palavras'),
            dcc.Graph(id='timeline-processamento'),
        ], style={'display': 'flex'}),
        
        # Terceira linha
        html.Div([
            dcc.Graph(id='heatmap-atividade'),
            dcc.Graph(id='boxplot-tamanhos'),
        ], style={'display': 'flex'}),
        
        # Quarta linha
        html.Div([
            dcc.Graph(id='barras-acumuladas'),
            dcc.Graph(id='scatter-tamanhos'),
        ], style={'display': 'flex'}),
        
        # Quinta linha
        html.Div([
            dcc.Graph(id='pie-distribuicao'),
            dcc.Graph(id='linha-tendencia'),
        ], style={'display': 'flex'}),
        
        # Sexta linha - Novos gráficos
        html.Div([
            dcc.Graph(id='cluster-analysis'),
            dcc.Graph(id='word-length-correlation'),
        ], style={'display': 'flex'}),
        
        # Sétima linha - Novos gráficos
        html.Div([
            dcc.Graph(id='daily-patterns'),
            dcc.Graph(id='origem-timeline'),
        ], style={'display': 'flex'}),
    ])
])

# Callbacks para cada gráfico
@app.callback(
    Output('palavras-por-hora', 'figure'),
    Input('palavras-por-hora', 'id')
)
def update_palavras_por_hora(id):
    fig = px.bar(
        df.groupby('hora').size().reset_index(),
        x='hora',
        y=0,
        title='Palavras Processadas por Hora',
        labels={'hora': 'Hora do Dia', '0': 'Quantidade de Palavras'}
    )
    return fig

@app.callback(
    Output('distribuicao-tamanhos', 'figure'),
    Input('distribuicao-tamanhos', 'id')
)
def update_distribuicao_tamanhos(id):
    fig = px.histogram(
        df,
        x='vector_size',
        title='Distribuição dos Tamanhos dos Vetores',
        labels={'vector_size': 'Tamanho do Vetor'}
    )
    return fig

@app.callback(
    Output('origem-palavras', 'figure'),
    Input('origem-palavras', 'id')
)
def update_origem_palavras(id):
    fig = px.pie(
        df.groupby('palavra_origem').size().reset_index(),
        values=0,
        names='palavra_origem',
        title='Distribuição por Origem das Palavras'
    )
    return fig

@app.callback(
    Output('timeline-processamento', 'figure'),
    Input('timeline-processamento', 'id')
)
def update_timeline(id):
    daily_counts = df.groupby('data').size().reset_index()
    fig = px.line(
        daily_counts,
        x='data',
        y=0,
        title='Timeline de Processamento',
        labels={'data': 'Data', '0': 'Palavras Processadas'}
    )
    return fig

@app.callback(
    Output('heatmap-atividade', 'figure'),
    Input('heatmap-atividade', 'id')
)
def update_heatmap(id):
    pivot = pd.crosstab(df['data'], df['hora'])
    fig = px.imshow(
        pivot,
        title='Heatmap de Atividade',
        labels={'x': 'Hora do Dia', 'y': 'Data'}
    )
    return fig

@app.callback(
    Output('boxplot-tamanhos', 'figure'),
    Input('boxplot-tamanhos', 'id')
)
def update_boxplot(id):
    fig = px.box(
        df,
        y='vector_size',
        title='Boxplot dos Tamanhos dos Vetores',
        labels={'vector_size': 'Tamanho do Vetor'}
    )
    return fig

@app.callback(
    Output('barras-acumuladas', 'figure'),
    Input('barras-acumuladas', 'id')
)
def update_barras_acumuladas(id):
    df_cum = df.groupby('data').size().cumsum().reset_index()
    fig = px.bar(
        df_cum,
        x='data',
        y=0,
        title='Total Acumulado de Palavras Processadas',
        labels={'data': 'Data', '0': 'Total Acumulado'}
    )
    return fig

@app.callback(
    Output('scatter-tamanhos', 'figure'),
    Input('scatter-tamanhos', 'id')
)
def update_scatter(id):
    fig = px.scatter(
        df,
        x='timestamp',
        y='vector_size',
        title='Dispersão de Tamanhos ao Longo do Tempo',
        labels={'timestamp': 'Data/Hora', 'vector_size': 'Tamanho do Vetor'}
    )
    return fig

@app.callback(
    Output('pie-distribuicao', 'figure'),
    Input('pie-distribuicao', 'id')
)
def update_pie_distribuicao(id):
    # Verifica se há variação nos tamanhos
    if df['vector_size'].nunique() < 5:
        # Se houver poucos valores únicos, usa value_counts diretamente
        counts = df['vector_size'].value_counts()
        labels = [f'Tamanho {int(size)}' for size in counts.index]
        
        fig = px.pie(
            values=counts.values,
            names=labels,
            title='Distribuição dos Tamanhos dos Vetores'
        )
    else:
        # Se houver variação suficiente, mantém a lógica original
        try:
            bins = pd.qcut(df['vector_size'], q=5, 
                          labels=['Muito Pequeno', 'Pequeno', 'Médio', 'Grande', 'Muito Grande'],
                          duplicates='drop')
            fig = px.pie(
                values=bins.value_counts(),
                names=bins.value_counts().index,
                title='Distribuição por Categorias de Tamanho'
            )
        except ValueError:
            # Fallback caso ainda ocorra algum erro
            counts = df['vector_size'].value_counts()
            fig = px.pie(
                values=counts.values,
                names=[f'Tamanho {int(size)}' for size in counts.index],
                title='Distribuição dos Tamanhos dos Vetores'
            )
    
    return fig

@app.callback(
    Output('linha-tendencia', 'figure'),
    Input('linha-tendencia', 'id')
)
def update_linha_tendencia(id):
    df_trend = df.groupby('data').agg({
        'vector_size': 'mean'
    }).reset_index()
    
    fig = px.line(
        df_trend,
        x='data',
        y='vector_size',
        title='Tendência do Tamanho Médio dos Vetores',
        labels={'data': 'Data', 'vector_size': 'Tamanho Médio'}
    )
    return fig

# Novos callbacks para os gráficos adicionais
@app.callback(
    Output('cluster-analysis', 'figure'),
    Input('cluster-analysis', 'id')
)
def update_cluster_analysis(id):
    # Preparar dados para clustering
    features = pd.DataFrame({
        'hora': df['hora'],
        'vector_size': df['vector_size'],
        'word_length': df['word'].str.len()
    })
    
    # Normalizar dados
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Aplicar K-means
    n_clusters = min(3, len(df))  # Evita erro se houver poucos dados
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(features_scaled)
    
    # Criar visualização
    fig = px.scatter_3d(
        data_frame=features,
        x='hora',
        y='vector_size',
        z='word_length',
        color=clusters,
        title='Análise de Clusters: Hora vs Tamanho do Vetor vs Tamanho da Palavra',
        labels={
            'hora': 'Hora do Dia',
            'vector_size': 'Tamanho do Vetor',
            'word_length': 'Tamanho da Palavra'
        }
    )
    return fig

@app.callback(
    Output('word-length-correlation', 'figure'),
    Input('word-length-correlation', 'id')
)
def update_word_length_correlation(id):
    df['word_length'] = df['word'].str.len()
    fig = px.scatter(
        df,
        x='word_length',
        y='vector_size',
        color='palavra_origem',
        title='Correlação: Tamanho da Palavra vs Tamanho do Vetor',
        labels={
            'word_length': 'Tamanho da Palavra',
            'vector_size': 'Tamanho do Vetor',
            'palavra_origem': 'Origem da Palavra'
        },
        trendline="ols"  # Adiciona linha de tendência
    )
    return fig

@app.callback(
    Output('daily-patterns', 'figure'),
    Input('daily-patterns', 'id')
)
def update_daily_patterns(id):
    # Análise de padrões diários com média móvel
    daily_data = df.groupby('data').agg({
        'vector_size': ['mean', 'std', 'count']
    }).reset_index()
    daily_data.columns = ['data', 'mean_size', 'std_size', 'count']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Média do tamanho dos vetores
    fig.add_trace(
        go.Scatter(
            x=daily_data['data'],
            y=daily_data['mean_size'],
            name="Média do Tamanho",
            line=dict(color='blue')
        )
    )
    
    # Quantidade de palavras processadas
    fig.add_trace(
        go.Scatter(
            x=daily_data['data'],
            y=daily_data['count'],
            name="Quantidade Processada",
            line=dict(color='red')
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title='Padrões Diários: Tamanho Médio e Quantidade',
        xaxis_title='Data',
        yaxis_title='Tamanho Médio do Vetor',
        yaxis2_title='Quantidade de Palavras'
    )
    
    return fig

@app.callback(
    Output('origem-timeline', 'figure'),
    Input('origem-timeline', 'id')
)
def update_origem_timeline(id):
    # Análise temporal por origem
    df_origem = df.groupby(['data', 'palavra_origem']).size().reset_index(name='count')
    
    fig = px.line(
        df_origem,
        x='data',
        y='count',
        color='palavra_origem',
        title='Evolução Temporal por Origem',
        labels={
            'data': 'Data',
            'count': 'Quantidade de Palavras',
            'palavra_origem': 'Origem da Palavra'
        }
    )
    
    return fig

# Novos callbacks para os gráficos adicionais
@app.callback(Output('new-graph-1', 'figure'), Input('new-graph-1', 'id'))
def update_word_frequency(id):
    word_freq = df['word'].value_counts().head(20)
    return px.bar(x=word_freq.index, y=word_freq.values,
                 title='Top 20 Palavras Mais Frequentes',
                 labels={'x': 'Palavra', 'y': 'Frequência'})

@app.callback(Output('new-graph-2', 'figure'), Input('new-graph-2', 'id'))
def update_weekly_pattern(id):
    df['dia_semana'] = df['timestamp'].dt.day_name()
    contagem = df['dia_semana'].value_counts()
    return px.bar(x=contagem.index, y=contagem.values,
                 title='Distribuição por Dia da Semana',
                 labels={'x': 'Dia', 'y': 'Quantidade'})

@app.callback(Output('new-graph-3', 'figure'), Input('new-graph-3', 'id'))
def update_word_length_dist(id):
    df['tamanho_palavra'] = df['word'].str.len()
    return px.histogram(df, x='tamanho_palavra',
                       title='Distribuição do Tamanho das Palavras',
                       labels={'tamanho_palavra': 'Número de Caracteres'})

@app.callback(Output('new-graph-4', 'figure'), Input('new-graph-4', 'id'))
def update_hourly_efficiency(id):
    df['palavras_por_hora'] = df.groupby(df['timestamp'].dt.hour)['word'].transform('count')
    return px.line(df.groupby(df['timestamp'].dt.hour)['palavras_por_hora'].mean(),
                  title='Eficiência por Hora do Dia')

@app.callback(Output('new-graph-5', 'figure'), Input('new-graph-5', 'id'))
def update_origem_word_length(id):
    return px.box(df, x='palavra_origem', y=df['word'].str.len(),
                 title='Tamanho das Palavras por Origem')

@app.callback(Output('new-graph-6', 'figure'), Input('new-graph-6', 'id'))
def update_monthly_trend(id):
    monthly = df.groupby(df['timestamp'].dt.strftime('%Y-%m')).size() # changed to strftime
    return px.line(monthly, title='Tendência Mensal de Processamento')

@app.callback(Output('new-graph-7', 'figure'), Input('new-graph-7', 'id'))
def update_processing_velocity(id):
    df['tempo_entre_processos'] = df['timestamp'].diff().dt.total_seconds()
    return px.histogram(df, x='tempo_entre_processos',
                       title='Distribuição do Tempo entre Processamentos')

@app.callback(Output('new-graph-8', 'figure'), Input('new-graph-8', 'id'))
def update_origem_hour_heatmap(id):
    heatmap_data = pd.crosstab(df['palavra_origem'], df['hora'])
    return px.imshow(heatmap_data,
                    title='Heatmap: Origem vs Hora do Dia')

@app.callback(Output('new-graph-9', 'figure'), Input('new-graph-9', 'id'))
def update_cumulative_origem(id):
    df_cum = df.groupby(['timestamp', 'palavra_origem']).size().unstack().fillna(0).cumsum()
    return px.line(df_cum, title='Crescimento Cumulativo por Origem')

@app.callback(Output('new-graph-10', 'figure'), Input('new-graph-10', 'id'))
def update_word_first_letter(id):
    first_letters = df['word'].str[0].value_counts()
    return px.pie(values=first_letters.values, names=first_letters.index,
                 title='Distribuição da Primeira Letra')

@app.callback(Output('new-graph-11', 'figure'), Input('new-graph-11', 'id'))
def update_processing_gaps(id):
    gaps = df['timestamp'].diff().dt.total_seconds().fillna(0)
    return px.scatter(x=df['timestamp'], y=gaps,
                     title='Gaps de Processamento ao Longo do Tempo')

@app.callback(Output('new-graph-12', 'figure'), Input('new-graph-12', 'id'))
def update_word_complexity(id):
    df['complexidade'] = df['word'].apply(lambda x: len(set(x))/len(x))
    return px.histogram(df, x='complexidade',
                       title='Distribuição da Complexidade das Palavras')

@app.callback(Output('new-graph-13', 'figure'), Input('new-graph-13', 'id'))
def update_hourly_boxplot(id):
    return px.box(df, x='hora', y=df['word'].str.len(),
                 title='Distribuição do Tamanho das Palavras por Hora')

@app.callback(Output('new-graph-14', 'figure'), Input('new-graph-14', 'id'))
def update_origem_efficiency(id):
    efficiency = df.groupby('palavra_origem')['vector_size'].agg(['mean', 'std'])
    return px.bar(efficiency, y='mean', error_y='std',
                 title='Eficiência por Origem (com Desvio Padrão)')

@app.callback(Output('new-graph-15', 'figure'), Input('new-graph-15', 'id'))
def update_word_pattern_analysis(id):
    df['tem_numero'] = df['word'].str.contains('\d').astype(int)
    return px.pie(df, names='tem_numero',
                 title='Proporção de Palavras com Números')

@app.callback(Output('new-graph-16', 'figure'), Input('new-graph-16', 'id'))
def update_processing_density(id):
    kde = stats.gaussian_kde(df['timestamp'].astype(np.int64))
    x_range = np.linspace(df['timestamp'].astype(np.int64).min(),
                         df['timestamp'].astype(np.int64).max(), 100)
    return px.line(x=pd.to_datetime(x_range), y=kde(x_range),
                  title='Densidade de Processamento')

@app.callback(Output('new-graph-17', 'figure'), Input('new-graph-17', 'id'))
def update_word_similarity(id):
    df['similar_next'] = df['word'].shift() == df['word']
    return px.line(df.groupby('data')['similar_next'].mean(),
                  title='Taxa de Palavras Similares por Dia')

@app.callback(Output('new-graph-18', 'figure'), Input('new-graph-18', 'id'))
def update_origem_time_distribution(id):
    return px.violin(df, x='palavra_origem', y='hora',
                    title='Distribuição de Horário por Origem')

@app.callback(Output('new-graph-19', 'figure'), Input('new-graph-19', 'id'))
def update_processing_stability(id):
    stability = df.groupby('data')['vector_size'].agg(['mean', 'std']).rolling(7).mean()
    return px.line(stability, title='Estabilidade do Processamento (Média Móvel 7 dias)')

@app.callback(Output('new-graph-20', 'figure'), Input('new-graph-20', 'id'))
def update_word_length_evolution(id):
    length_evolution = df.groupby('data')['word'].apply(lambda x: x.str.len().mean())
    return px.line(length_evolution, title='Evolução do Tamanho Médio das Palavras')

@app.callback(Output('new-graph-21', 'figure'), Input('new-graph-21', 'id'))
def update_origem_success_rate(id):
    success_rate = df.groupby(['data', 'palavra_origem']).size().unstack(fill_value=0)
    success_rate = success_rate.div(success_rate.sum(axis=1), axis=0)
    return px.area(success_rate, title='Taxa de Sucesso por Origem')

@app.callback(Output('new-graph-22', 'figure'), Input('new-graph-22', 'id'))
def update_processing_anomalies(id):
    z_scores = np.abs(stats.zscore(df['vector_size']))
    df['is_anomaly'] = z_scores > 3
    return px.scatter(df, x='timestamp', y='vector_size', color='is_anomaly',
                     title='Detecção de Anomalias no Processamento')

reports = [] # Initialize reports list

# Salvar todos os gráficos como HTML estático
def save_reports():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Adicionar novos callbacks à lista de reports
    reports.extend([
        (update_word_frequency, 'word_frequency'),
        (update_weekly_pattern, 'weekly_pattern'),
        (update_word_length_dist, 'word_length_dist'),
        (update_hourly_efficiency, 'hourly_efficiency'),
        (update_origem_word_length, 'origem_word_length'),
        (update_monthly_trend, 'monthly_trend'),
        (update_processing_velocity, 'processing_velocity'),
        (update_origem_hour_heatmap, 'origem_hour_heatmap'),
        (update_cumulative_origem, 'cumulative_origem'),
        (update_word_first_letter, 'word_first_letter'),
        (update_processing_gaps, 'processing_gaps'),
        (update_word_complexity, 'word_complexity'),
        (update_hourly_boxplot, 'hourly_boxplot'),
        (update_origem_efficiency, 'origem_efficiency'),
        (update_word_pattern_analysis, 'word_pattern_analysis'),
        (update_processing_density, 'processing_density'),
        (update_word_similarity, 'word_similarity'),
        (update_origem_time_distribution, 'origem_time_distribution'),
        (update_processing_stability, 'processing_stability'),
        (update_word_length_evolution, 'word_length_evolution'),
        (update_origem_success_rate, 'origem_success_rate'),
        (update_processing_anomalies, 'processing_anomalies'),
        (update_palavras_por_hora, 'palavras_por_hora'),
        (update_distribuicao_tamanhos, 'distribuicao_tamanhos'),
        (update_origem_palavras, 'origem_palavras'),
        (update_timeline, 'timeline_processamento'),
        (update_heatmap, 'heatmap_atividade'),
        (update_boxplot, 'boxplot_tamanhos'),
        (update_barras_acumuladas, 'barras_acumuladas'),
        (update_scatter, 'scatter_tamanhos'),
        (update_pie_distribuicao, 'pie_distribuicao'),
        (update_linha_tendencia, 'linha_tendencia'),
        (update_cluster_analysis, 'cluster_analysis'),
        (update_word_length_correlation, 'word_length_correlation'),
        (update_daily_patterns, 'daily_patterns'),
        (update_origem_timeline, 'origem_timeline')
    ])
    
    for callback, name in reports:
        fig = callback(None)
        fig.write_html(f'reports/{name}_{timestamp}.html')

if __name__ == '__main__':
    save_reports()  # Salvar versões estáticas
    app.run_server(debug=True)  # Iniciar servidor Dash
