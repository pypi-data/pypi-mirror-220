from anya_dash import *
from dash import Dash, Output, Input, State, html
from dash.exceptions import PreventUpdate


app = Dash(__name__)
app.layout = AnyaTheme(
    AnyaRow(
        AnyaCol(
            [
                AnyaSpace(
                    [
                        AnyaButton('Open Modal', type='primary', id='modal-btn'),
                        AnyaButton('Execute JS', type='primary', id='js-btn'),
                        AnyaExecuteJs(id='execute-js')
                    ]
                ),
                AnyaModal(
                    'Modal Content',
                    id='modal',
                    title='Title',
                    visible=False
                ),
                AnyaRow(
                    AnyaCol(
                        AnyaTabs(
                            items=[
                                {
                                    'key': f'tab{i}',
                                    'label': f'tab{i}'
                                }
                                for i in range(1, 6)
                            ],
                            id='tabs',
                            defaultActiveKey='tab1',
                            children=html.Div(id='activeTab'),
                            wrapperStyle={
                                'padding': '20px',
                                'width': '600px'
                            },
                            childCardStyle={
                                'backgroundColor': '#efeffb',
                                'aligItems': 'center',
                                'justifyContent': 'center',
                                'display': 'flex',
                            }
                        ),
                        span=12
                    )
                ),
                AnyaRow(
                    [
                        AnyaCol(
                            AnyaCard(
                                children='Card without any title',
                                style={'height': '130px'}
                            ),
                            span=8
                        ),
                        AnyaCol(
                            AnyaCard(
                                title='Title',
                                children='Card with a title',
                                style={'height': '130px'},
                                size='small',
                                extraLinkHref='https://github.com/AnyaIp',
                                extraLinkText='Anya',
                            ),
                            span=8
                        ),
                        AnyaCol(
                            AnyaCard(
                                children='Card without external link',
                                style={'height': '130px'},
                                size='small',
                                extraLinkHref='https://github.com/AnyaIp',
                                extraLinkText='Anya',
                            ),
                            span=8
                        ),
                    ],
                    gutter=10,
                    style={'marginBottom': '10px'}
                ),
                AnyaRow(
                    [
                        AnyaCol(
                            AnyaCard(
                                'backgroundColor: #f9f9f9',
                                title='Title Ya',
                                headStyle={'backgroundColor': '#de5886', 'color': '#fff',
                                           'paddingTop': '0px', 'paddingBottom': '0px'},
                                bodyStyle={
                                    'backgroundColor': '#f9f9f9', 'height': '150px'},
                                size='small',
                                extraLinkHref='https://github.com/AnyaIp',
                                extraLinkText='Anya',
                                extraLinkStyle={'color': '#fff'}
                            ),
                            span=8
                        ),
                        AnyaCol(
                            AnyaCard(
                                children='Hoverable card with a cover image',
                                coverImgSrc='https://c4.wallpaperflare.com/wallpaper/393/423/638/anya-forger-spy-x-family-anime-girls-hd-wallpaper-preview.jpg',
                                hoverable=True
                            ),
                            span=8
                        ),
                        AnyaCol(
                            AnyaCard(
                                children='hey ya',
                                coverImgSrc='https://c4.wallpaperflare.com/wallpaper/393/423/638/anya-forger-spy-x-family-anime-girls-hd-wallpaper-preview.jpg',
                                hoverable=True,
                                title='Title Ya',
                                bodyStyle={'backgroundColor': '#fff5f7'},
                            ),
                            span=8
                        ),
                    ],
                    gutter=10,
                    style={'marginBottom': '10px'}
                ),
                AnyaRow(
                    [
                        AnyaCol(
                            AnyaCollapse(
                                AnyaParagraph(
                                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                                ),
                                bordered=False,
                                title='Collapse 1'
                            ),
                            span=8
                        ),
                        AnyaCol(
                            AnyaCollapse(
                                AnyaParagraph(
                                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                                ),
                                title='Collapse 1'
                            ),
                            span=8
                        ),
                        AnyaCol(
                            AnyaCollapse(
                                AnyaParagraph(
                                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                                ),
                                title='Collapse 1',
                                style={'backgroundColor': '#fff5f7'}
                            ),
                            span=8
                        )
                    ],
                    gutter=10
                )
            ],
            lg={'span': 18, 'offset': 3},
            md={'span': 20, 'offset': 2},
            xs=24,
            style={
                'backgroundColor': '#fff',
                'height': '100vh',
                'padding': '16px'
            }
        ),
        style={'backgroundColor': '#f3f6ff'}
    )
)


@app.callback(
    Output('activeTab', 'children'),
    Input('tabs', 'activeKey'),
    prevent_initial_call=True
)
def returnActiveTab(value):
    return value

@app.callback(
    Output('modal', 'visible'),
    Input('modal-btn', 'n_clicks'),
    prevent_initial_callback=True
)
def showModal(n_clicks):
    if n_clicks:
        return True
    raise PreventUpdate

@app.callback(
    Output('execute-js', 'jsString'),
    Input('js-btn', 'n_clicks')
)
def executejs(n_clicks):
    if n_clicks:
        return 'alert("Hello World!");'
    else:
        raise PreventUpdate
    


if __name__ == '__main__':
    app.run_server(debug=True)
