from anya_dash import *
from dash import Dash, Output, Input, State, html, ALL, ctx
import pandas as pd


df = pd.read_csv('test.csv').head(50)
df = df[['First Name', 'Last Name', 'Sex', 'Email', 'Job Title']]
df.columns = ['first_name', 'last_name', 'sex', 'email', 'title']


def df_to_source(
    df,
    rename={}
):
    cols = []
    for col in df.columns:
        col_dt = {'dataIndex': col}
        if col in rename:
            col_dt.update(rename[col])
        else:
            col_dt.update({'title': col})
        cols.append(col_dt)
    df.insert(0, 'key', range(1, len(df) + 1))
    data = df.to_dict('records')
    return cols, data


cols, data = df_to_source(df, rename={
    'age': {'align': 'center', 'title': 'Age'},
    'sex': {'title': 'Sex', 'align': 'center'},
    'email': {'title': 'Email'},
    'title': {'title': 'Job Title'},
    'first_name': {'title': 'First Name'},
    'last_name': {'title': 'Last Name'}
})

cols2 = [
    {'dataIndex': 'first_name', 'title': 'Name', 'colSpan': 2,
        'rowSpan': {0: 2, 1: 0}, 'colSpanRow': {2: 1}},
    {'dataIndex': 'last_name', 'title': 'Last Name', 'colSpan': 0,
        'rowSpan': {0: 2, 1: 0}, 'colSpanRow': {2: 1}},
    {'dataIndex': 'sex', 'title': 'Sex', 'rowSpan': {
        0: 2, 1: 0}, 'align': 'center', 'colSpanRow': {2: 2}},
    {'dataIndex': 'title', 'title': 'Job Title',
        'rowSpan': {3: 2, 4: 0}, 'colSpanRow': {2: 0}}
]

data2 = [
    {'key': 'sh', 'first_name': 'Shelby', 'last_name': 'Terrell',
     'sex': AnyaTag('Male', color='blue'), 'title': 'Games developer'},
    {'key': 'se', 'title': 'Phytotherapist'},
    {'key': 'kr', 'first_name': 'Kristine',
        'last_name': 'Travis', 'sex': '', 'title': 'Homeopath', },
    {'key': 'ye', 'first_name': 'Yesenia', 'last_name': 'Martinez',
        'sex': AnyaTag('Male', color='blue'),  'title': 'Market researcher'},
    {'key': 'lo', 'first_name': 'Marry', 'last_name': 'Todd',
        'sex': AnyaTag('Female', color='pink'), 'title': 'Market researcher'}
]

app = Dash(__name__)
app.layout = AnyaTheme(
    AnyaRow(
        AnyaCol(
            [
                AnyaTitle('Basic Usage', level=4),
                AnyaTable(
                    columns=cols,
                    data=data,
                    pagination={
                        'pageSize': 5,
                        'hideOnSinglePag': True,
                        'showSizeChanger': False,
                        # 'position': 'topRight'
                    },
                    size='small',
                    bordered=True,
                    id='table-1'
                ),
                html.Hr(),
                AnyaTitle('colSpan & rowSpan', level=4),
                AnyaTable(
                    columns=cols2,
                    data=data2,
                    pagination=False,
                    size='small',
                    bordered=True
                ),
            ],
            lg={'span': 18, 'offset': 3},
            md={'span': 20, 'offset': 2},
            xs=24,
            style={
                'backgroundColor': '#fff',
                'padding': '32px',
                'minHeight': '100vh'
            }
        ),
        style={'backgroundColor': '#f3f6ff'}
    )
)


if __name__ == '__main__':
    app.run_server(debug=True)
