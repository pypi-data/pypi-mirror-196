from rich.console import Console
from rich.table import Table


def partialy_sorted(_list: list, order: list) -> list:
    unordered = [e for e in _list if e not in order]
    mapping = order + unordered
    return sorted(_list, key=mapping.index)


def create_table(_list: list[dict], columns_order: list[str]):
    headers = partialy_sorted(list({key for _dict in _list for key in _dict.keys()}), order=columns_order)

    table = Table(*headers, show_lines=True)
    for _dict in _list:
        table.add_row(*[_dict.get(key) for key in headers])
    return table


def show(result: list[dict]) -> None:
    print("\nAdditional tags will look like:")
    console = Console()
    table = create_table(result, columns_order=["eni", "svc", "name"])
    console.print(table, new_line_start=True)
