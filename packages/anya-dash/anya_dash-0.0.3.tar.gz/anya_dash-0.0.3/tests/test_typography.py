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

app.layout = AnyaTheme(
    [
        AnyaAffix(topNavBar),
        AnyaLayout(
            [
                AnyaContent(
                    AnyaRow(
                        AnyaCol(
                            AnyaSpace(
                                [
                                    AnyaTitle('H1. Anya Forger (Gradient)',
                                              level=1, className='text-gradient'),
                                    AnyaParagraph(
                                        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                                    ),
                                    AnyaParagraph(
                                        'Sagittis vitae et leo duis ut diam quam nulla porttitor. In tellus integer feugiat scelerisque varius morbi enim. Tempor orci eu lobortis elementum nibh tellus molestie. Euismod lacinia at quis risus sed vulputate odio. Faucibus nisl tincidunt eget nullam non nisi. Vel elit scelerisque mauris pellentesque pulvinar pellentesque habitant. Aliquam ultrices sagittis orci a scelerisque. Molestie at elementum eu facilisis sed odio morbi. Et netus et malesuada fames ac turpis egestas maecenas pharetra. Risus ultricies tristique nulla aliquet enim. Ipsum dolor sit amet consectetur adipiscing elit pellentesque. Tellus in hac habitasse platea dictumst vestibulum rhoncus est.'
                                    ),
                                    AnyaTitle('H2. Anya Forger (Success)',
                                              level=2, type='success'),
                                    AnyaText(
                                        'Non diam phasellus vestibulum lorem sed risus ultricies tristique nulla. Bibendum neque egestas congue quisque egestas diam in arcu. Congue nisi vitae suscipit tellus mauris a diam maecenas sed.',
                                        code=True,
                                        type='success'),
                                    AnyaTitle(
                                        'H3. Anya Forger (Danger, Italic)', level=3, type='danger', italic=True),
                                    AnyaParagraph(
                                        AnyaText(
                                            'Blandit cursus risus at ultrices mi. Integer malesuada nunc vel risus commodo viverra maecenas accumsan. Habitant morbi tristique senectus et netus et malesuada fames. Interdum velit euismod in pellentesque massa placerat duis ultricies lacus. Suscipit adipiscing bibendum est ultricies integer. Lectus nulla at volutpat diam ut venenatis tellus in metus. A pellentesque sit amet porttitor eget dolor morbi non arcu. Aliquam purus sit amet luctus.',
                                            type='secondary'
                                        )
                                    ),
                                    AnyaTitle('H4. Anya Forger (Warning, Strikethrough)',
                                              level=4, strikethrough=True, type='warning'),
                                    AnyaTitle(
                                        'H5. Anya Forger (Secondary)', level=5, type='secondary')
                                ],
                                direction='vertical',
                                size=0
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


if __name__ == '__main__':
    app.run_server(debug=True)
