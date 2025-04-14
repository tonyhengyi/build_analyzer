#!/usr/bin/env python3
import dash
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import json
from collections import defaultdict

# 1. 加载数据
def load_data():
    # 系统调用统计
    syscalls = pd.read_csv("/home/zhy_clound/build_analyzer/utils/syscall_stats.csv")
    syscalls['percentage'] = (syscalls['count'] / syscalls['count'].sum() * 100).round(2)
    
    # 依赖关系
    with open("/home/zhy_clound/build_analyzer/utils/sqlite_dependencies.json") as f:
        deps = json.load(f)
    
    # 转换依赖数据为网络图格式
    edges = []
    for src, headers in deps.items():
        for hdr in headers:
            edges.append({'source': src, 'target': hdr, 'value': 1})
    
    return syscalls, pd.DataFrame(edges)

syscall_df, deps_df = load_data()

# 2. 创建Dash应用
app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Tabs([
        # 标签页1: 系统调用分析
        dcc.Tab(label='系统调用统计', children=[
            html.Div([
                html.H3("系统调用频率分析", style={'textAlign': 'center'}),
                dcc.Graph(id='syscall-bar'),
                dcc.Graph(id='syscall-pie'),
                html.Div([
                    dcc.Slider(
                        id='topn-slider',
                        min=5,
                        max=20,
                        step=1,
                        value=10,
                        marks={i: str(i) for i in range(5, 21, 5)}
                    )
                ], style={'padding': 20})
            ])
        ]),
        
        # 标签页2: 依赖关系分析
        dcc.Tab(label='依赖关系图', children=[
            html.Div([
                html.H3("源码文件依赖关系", style={'textAlign': 'center'}),
                dcc.Dropdown(
                    id='file-selector',
                    options=[{'label': f, 'value': f} for f in deps_df['source'].unique()],
                    multi=True,
                    placeholder="选择源文件..."
                ),
                dcc.Graph(id='deps-network'),
                html.Div(id='deps-info', style={'marginTop': 20})
            ], style={'padding': 20})
        ])
    ])
])

# 3. 回调函数
# 系统调用标签页
@app.callback(
    [Output('syscall-bar', 'figure'),
     Output('syscall-pie', 'figure')],
    [Input('topn-slider', 'value')]
)
def update_syscall_charts(topn):
    dff = syscall_df.head(topn)
    
    bar = px.bar(
        dff, x='count', y='syscall', orientation='h',
        title=f'Top {topn} 系统调用', color='count',
        color_continuous_scale='Viridis'
    )
    
    pie = px.pie(
        dff, names='syscall', values='count',
        title='调用占比', hole=0.4
    )
    
    return bar, pie

# 依赖关系标签页
@app.callback(
    [Output('deps-network', 'figure'),
     Output('deps-info', 'children')],
    [Input('file-selector', 'value')]
)
def update_deps_graph(selected_files):
    if not selected_files:
        # 显示全图
        fig = px.scatter(
            pd.concat([deps_df['source'], deps_df['target']]).value_counts().reset_index(),
            x='index', y='count',
            title='所有文件依赖概览'
        )
        return fig, "请从下拉菜单选择具体文件查看详细依赖"
    
    # 生成网络图
    filtered_df = deps_df[deps_df['source'].isin(selected_files)]
    
    fig = px.treemap(
        filtered_df,
        path=['source', 'target'],
        title=f'{len(selected_files)}个文件的依赖关系'
    )
    
    # 统计信息
    stats = html.Div([
        html.P(f"选中文件: {', '.join(selected_files)}"),
        html.P(f"涉及头文件: {filtered_df['target'].nunique()}个"),
        html.P(f"总依赖关系: {len(filtered_df)}条")
    ])
    
    return fig, stats

# 4. 启动应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)