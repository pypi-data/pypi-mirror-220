from anya_dash import *
from dash import Dash, Output, Input, State, html


app = Dash(__name__)
app.layout = AnyaTheme(
    AnyaRow(
        AnyaCol(
            [
                AnyaTitle('Switch', level=3),
                AnyaSpace(
                    [
                        AnyaSwitch(
                            checkedChildren='Open',
                            unCheckedChildren='Close',
                            id='switch'
                        ),
                        AnyaButton('Swith: Close', type='dashed',
                                   id='switch-btn-ouput'),
                        AnyaSwitch(disabled=True, checked=True),
                    ],
                    direction='horizontal',
                    size='small',
                    align='center'
                ),
                html.Hr(),
                AnyaTitle('Date Picker', level=3),
                AnyaSpace(
                    [
                        AnyaDateRangePicker(
                            id='date-picker',
                            placement='bottomRight',
                            style={
                                'width': 275
                            }
                        ),
                        AnyaButton('Selected date: ...', type='dashed', id='date-picker-ouput'),
                    ],
                    direction='horizontal',
                    align='center'
                ),
                html.Hr(),
                AnyaTitle('Dropdowns', level=3),
                AnyaSpace(
                    [
                        AnyaSelect(
                            options=[
                                {
                                    'label': f'Choice {i}',
                                    'value': f'{i}'
                                }
                                for i in range(1, 6)
                            ],
                            defaultValue='1',
                            style={
                                'width': 200
                            },
                            id='select-1'
                        ),
                        AnyaSelect(
                            options=[
                                {
                                    'label': f'Choice {i}',
                                    'value': f'{i}'
                                }
                                for i in range(1, 6)
                            ],
                            mode='multiple',
                            value=['1', '3'],
                            style={
                                'width': 300
                            },
                            id='select-2'
                        ),
                        AnyaSelect(
                            id='dropdown',
                            options=[
                                {
                                    'group': 'Group 1',
                                    'options': [
                                        {
                                            'label': f'Choice 1-{i}',
                                            'value': f'1-{i}'
                                        }
                                        for i in range(1, 4)
                                    ]
                                },
                                {
                                    'group': 'Group 2',
                                    'options': [
                                        {
                                            'label': f'Choice 2-{i}',
                                            'value': f'2-{i}'
                                        }
                                        for i in range(1, 4)
                                    ]
                                }
                            ],
                            placeholder='Grouped Options',
                            style={
                                'width': 200
                            }
                        ),
                        AnyaButton('Selected value: ...',
                                   type='dashed', id='dropdown-btn-ouput'),
                    ],
                    direction='vertical',
                    size='small'
                ),
                html.Hr(),
                AnyaTitle('Radio Groups', level=3),
                AnyaRadioGroup(
                    options=[
                        {
                            'label': f'Choice {c}',
                            'value': c
                        }
                        for c in list('ABCDEF')
                    ],
                    defaultValue='A',
                    id='radio',
                    direction='vertical'
                ),
                AnyaButton('Selected value: ...',
                           type='dashed', id='radio-btn-ouput'),
                html.Hr(),
                AnyaTitle('Checkboxes', level=3),
                AnyaSpace(
                    [
                        AnyaCheckboxGroup(
                            options=[
                                {
                                    'label': f'Choice {i}',
                                    'value': f'{i}'
                                }
                                for i in range(5)
                            ],
                            value=[f'{i}' for i in range(5)],
                            id='checkbox',
                            includeSelectAll=True
                        ),
                        AnyaButton('Selected value: All',
                                   type='dashed', id='checkbox-btn-ouput'),
                    ],
                    align='center'
                ),
                AnyaTitle('Input Boxes', level=3),
                AnyaSpace(
                    [
                        AnyaInput(placeholder='mode="default"',
                                  style={'width': '500px'}),
                        AnyaInput(
                            placeholder='mode="search"',
                            style={'width': '500px'},
                            mode='search'
                        ),
                        AnyaInput(
                            placeholder='mode="text-area"',
                            style={'width': '500px'},
                            mode='text-area'
                        ),
                        AnyaInput(
                            placeholder='mode="password"',
                            style={'width': '500px'},
                            mode='password'
                        ),
                        AnyaInputNumber(
                            step=0.001,
                            defaultValue=0,
                            placeholder='step=0.001',
                            style={'width': '120px'},
                        )
                    ],
                    size='small',
                    direction='vertical'
                ),
                html.Hr(),
                AnyaTitle('Sliders', level=3),
                AnyaSpace(
                    [
                        AnyaSlider(
                            id='slider-point',
                            range=False,
                            min=0,
                            max=100,
                            tooltipVisible=True,
                            defaultValue=50,
                            style={
                                'width': 300
                            }
                        ),
                        AnyaSlider(
                            id='slider-range',
                            range=True,
                            tooltipVisible=True,
                            min=0,
                            max=100,
                            marks={0: '0', 100: '100'},
                            defaultValue=[20, 70],
                            style={
                                'width': 300
                            }
                        )

                    ],
                    direction='vertical',
                    size='small'
                )
            ],
            lg={'span': 18, 'offset': 3},
            md={'span': 20, 'offset': 2},
            xs=24,
            style={
                'backgroundColor': '#fff',
                'padding': '32px'
            }
        ),
        style={'backgroundColor': '#f3f6ff'}
    )
)


@app.callback(
    Output('switch-btn-ouput', 'children'),
    Input('switch', 'checked')
)
def dis_collapse(colapsed):
    return 'Swith: {}'.format(str(colapsed).title())


@app.callback(
    Output('dropdown-btn-ouput', 'children'),
    Input('dropdown', 'value')
)
def dis_collapse(value):
    return 'Selected value: {}'.format(value)


@app.callback(
    Output('radio-btn-ouput', 'children'),
    Input('radio', 'value')
)
def dis_collapse(value):
    return 'Selected value: {}'.format(value)


@app.callback(
    Output('checkbox-btn-ouput', 'children'),
    Input('checkbox', 'value')
)
def dis_collapse(value):
    return 'Selected value: {}'.format('; '.join(value))

@app.callback(
    Output('date-picker-ouput', 'children'),
    Input('date-picker', 'value')
)
def dis_collapse(value):
    if not value:
        value = []
    return 'Selected dates: {}'.format(' to '.join(value))


if __name__ == '__main__':
    app.run_server(debug=True)
