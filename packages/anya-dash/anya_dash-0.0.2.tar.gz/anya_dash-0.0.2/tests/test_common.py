from anya_dash import *
from dash import Dash, Output, Input, State, html


app = Dash(__name__)


tags = [
    AnyaTag(
        children=color,
        color=color
    )
    for color in [
        'magenta',
        'red',
        'volcano',
        'orange',
        'gold',
        'lime',
        'green',
        'cyan',
        'blue',
        'geekblue',
        'purple'
    ]
]

tags += [AnyaTag('linked tag', color='#6366f1',
                 href='https://github.com/AnyaIp')]

app.layout = AnyaTheme(
    [
        AnyaLayout(
            [
                AnyaContent(
                    AnyaRow(
                        AnyaCol(
                            html.Div(
                                [
                                    AnyaTitle('Tags', level=3),
                                    AnyaSpace(
                                        tags,
                                        wrap=True,
                                        size='small'
                                    ),
                                    html.Hr(),
                                    AnyaTitle('Buttons', level=3),
                                    AnyaSpace(
                                        [
                                            AnyaButton('primary', type='primary'),
                                            AnyaButton('dagner', danger=True),
                                            AnyaButton('success', success=True),
                                            AnyaButton('ghost', type='ghost'),
                                            AnyaButton('linked button', info=True, href='https://github.com/AnyaIp'),
                                            AnyaButton('click test', pink=True, id='click-btn'),
                                            AnyaButton('No. of clicks: 0', type='dashed', id='nclicks-btn', n_clicks=0),
                                        ],
                                        wrap=True,
                                        size='small'
                                    ),
                                    html.Hr(),
                                    AnyaTitle('Icons', level=3),
                                    AnyaSpace(
                                        [
                                            AnyaIcon(icon='FullscreenOutlined', style={'fontSize': '20px', 'color': '#6366f1'}),
                                            AnyaIcon(icon='HeartTwoTone', style={'fontSize': '20px'}),
                                            AnyaIcon(icon='CalendarOutlined', style={'fontSize': '20px', 'color': '#6366f1'})
                                        ],
                                        wrap=True,
                                        size='small'          
                                    )

                                ]
                            ),
                            lg={'span': 18, 'offset': 3},
                            md={'span': 20, 'offset': 2},
                            xs=24,
                            style={
                                'backgroundColor': '#fff',
                                'height': '100vh',
                                'padding': '16px'
                            }
                        )
                    ),
                    backgroundColor='#f3f6ff',
                    id='anya-content'
                ),
                AnyaFooter('Footer', textAlign='center')
            ],
            id='content-container',
            style={'backgroundColor': '#fff'}
        ),

    ]
)

@app.callback(
    Output('nclicks-btn', 'children'),
    Input('click-btn', 'n_clicks'),
    prevent_initial_call=True
)
def count_click(val):
    return 'No. of clicks: {}'.format(val)


if __name__ == '__main__':
    app.run_server(debug=True)
