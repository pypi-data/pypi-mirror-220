from anya_dash import *
from dash import Dash, Output, Input, State, html


app = Dash(__name__)

topNavBar = AnyaMenu(
    id='menu-demo',
    isTopNav=True,
    currentKey='anya-main',
    style={
        'fontSize': 13
    },
    menuItems=[
        {
            'component': 'Item',
            'props': {
                'key': 'anya-main',
                'title': 'Anya Main',
                'href': 'https://github.com/AnyaIp',
            }
        },
        {
            'component': 'SubMenu',
            'props': {
                'key': 'anya-sub',
                'title': 'Anya Sub'
            },
            'children': [
                {
                    'component': 'ItemGroup',
                    'props': {
                        'key': f'anya-sub-{item_group}',
                        'title': f'Anya Sub {item_group}'
                    },
                    'children': [
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'anya-sub-{item_group}-{item}',
                                'title': f'Anya Sub {item_group}-{item}'
                            }
                        }
                        for item in range(1, 3)
                    ]
                }
                for item_group in range(1, 3)
            ]
        }
    ],
    mode='horizontal'
)

sideNavBar = AnyaMenu(
    id='menu-demo-side',
    isTopNav=False,
    mode='inline',
    currentKey='anya-main',
    style={
        'height': '100%'
    },
    menuItems=[
        {
            'component': 'Item',
            'props': {
                'key': 'anya-main',
                'title': 'Anya Main',
                'href': 'https://github.com/AnyaIp',
            }
        },
        {
            'component': 'SubMenu',
            'props': {
                'key': 'anya-sub',
                'title': 'Anya Sub'
            },
            'children': [
                {
                    'component': 'ItemGroup',
                    'props': {
                        'key': f'anya-sub-{item_group}',
                        'title': f'Anya Sub-{item_group}'
                    },
                    'children': [
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'anya-sub-{item_group}-{item}',
                                'title': f'Anya Sub-{item_group}-{item}'
                            }
                        }
                        for item in range(1, 3)
                    ]
                }
                for item_group in range(1, 3)
            ]
        }
    ],
)

app.layout = AnyaTheme(
    [
        AnyaAffix(topNavBar),
        AnyaLayout(
            [
                AnyaSider(
                    sideNavBar,
                    theme='light',
                    collapsible=True,
                    id='anya-sider',
                    isFixed=True,
                    offsetTop=46,
                    width=300
                ),
                AnyaLayout(
                    [
                        AnyaAffix(
                            AnyaHeader(
                                'Header',
                                collapsible=True,
                                id='anya-header'
                            ),
                            offsetTop=46,
                            className='affix'
                        ),
                        AnyaContent(
                            'Content',
                            style={
                                'height': '100vh',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                            },
                            backgroundColor='#f3f6ff',
                            id='anya-content'
                        ),
                        AnyaFooter('Footer', textAlign='center')
                    ],
                    id='content-container'
                ),
            ],
            hasSider=True,
            style={'backgroundColor': '#fff'}
        )
    ]
)


@app.callback(
    [
        Output('anya-sider', 'collapsed'),
        Output('content-container', 'style')
    ],
    Input('anya-header', 'isClicked')
)
def collapse_sider(isClicked):
    if isClicked:
        style = {'marginLeft': 0, 'transition': '0.5s'}
    else:
        style = {'marginLeft': 300}
    return isClicked, style


if __name__ == '__main__':
    app.run_server(debug=True)
