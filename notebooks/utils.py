import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def _adapt(df, **kwargs):
    for column, dtype in kwargs.get('types', {}).items():
        df[column] = df[column].astype(dtype)
    for column, func in kwargs.get('transforms', {}).items():
        df[column] = df[column].apply(func)

    if 'sort' in kwargs:
        df.sort_values(by=kwargs.get('sort'), inplace=True)

    return df


def prepare(df, **kwargs):
    prepared = df.copy()
    prepared = prepared.fillna(value=kwargs.get('na_substitutions', {}))
    prepared = _adapt(prepared, **kwargs)

    return prepared


def aggregate(df, **kwargs):
    agg_df = df.groupby(kwargs.get('by')).aggregate(**kwargs.get('agg')).reset_index()
    agg_df = _adapt(agg_df, **kwargs)

    return agg_df


def parse_flags(value):
    return value.strip().split('|')


def plot(df, x, y, is_timeseries=False, **kwargs):
    fig, ax = plt.subplots(1, 1, figsize=(16, 9), constrained_layout=True)

    if is_timeseries:
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_minor_locator(mdates.HourLocator(interval=6))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%a %d'))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
        ax.get_xaxis().set_tick_params(which='major', pad=15)
        ax.grid(True)

    if 'title' in kwargs:
        ax.set_title(kwargs['title'])
    if 'xlabel' in kwargs:
        ax.set_ylabel(kwargs['xlabel'])
    if 'ylabel' in kwargs:
        ax.set_ylabel(kwargs['ylabel'])

    column_order = {column: k for k, column in enumerate(df.columns)}
    data = df.to_numpy()

    if isinstance(y, str):
        y = {y: y}

    for key, value in y.items():
        ax.plot(data[:, column_order[x]], data[:, column_order[value]], label=key)
    if len(y) > 1:
        ax.legend()
    if 'path' in kwargs:
        plt.savefig(kwargs['path'], bbox_inches='tight')
    plt.show()


def scatter(df, x, y, **kwargs):
    fig, ax = plt.subplots(1, 1, figsize=(16, 9), constrained_layout=True)

    if 'title' in kwargs:
        ax.set_title(kwargs['title'])
    if 'xlabel' in kwargs:
        ax.set_ylabel(kwargs['xlabel'])
    if 'ylabel' in kwargs:
        ax.set_ylabel(kwargs['ylabel'])

    column_order = {column: k for k, column in enumerate(df.columns)}
    data = df.to_numpy()

    if isinstance(y, str):
        y = {y: y}

    for key, value in y.items():
        ax.scatter(data[:, column_order[x]], data[:, column_order[value]], label=key, alpha=kwargs.get('alpha', 1))
    if len(y) > 1:
        ax.legend()
    if 'path' in kwargs:
        plt.savefig(kwargs['path'], bbox_inches='tight')
    plt.show()
