import pickle
from functools import wraps
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

primitives = (int, str, bool, float)
forbidden_plt_fns = tuple()


def is_primitive(thing):
    return any(isinstance(thing, primitive) for primitive in primitives)


script_template = """import numpy as np
import matplotlib.pyplot as plt
from smartplot import load_pickle


{load_variables_code}

{do_plot_code}
"""
pickle_load_template = "{var_name} = load_pickle('{var_name}.pkl')"


def insert_next_available(dict_, key, val):
    postfix = ''
    ind = 1
    while key + postfix in dict_:
        ind += 1
        postfix = str(ind)

    dict_[key + postfix] = val
    return key + postfix


class SmartDict(dict):
    def __init__(self, dict_=None):
        super().__init__()
        self.actual_keys = {}

        if dict_:
            for k, v in dict_.items():
                self[k] = v

    def __getitem__(self, item):
        return super().__getitem__(id(item))

    def __contains__(self, item):
        return super().__contains__(id(item))

    def __setitem__(self, key, value):
        super().__setitem__(id(key), value)
        self.actual_keys[id(key)] = key

    def keys(self):
        return self.actual_keys.values()

    def items(self):
        return ((k, self[k]) for k in self.keys())

    def update(self, dict_, reverse=False):
        for k, v in dict_.items():
            if reverse:
                k, v = v, k
            self[k] = v

    @property
    def reverse(self):
        reverse = SmartDict()
        for k, v in self.items():
            reverse[v] = k
        return reverse


class Call:
    def __init__(
        self,
        fn_name,
        call_args,
        call_kwargs,
    ):
        self.fn_name = fn_name
        self.call_args = call_args
        self.call_kwargs = call_kwargs

        self.recall_args = []
        self.recall_kwargs = {}

    def find_or_name_obj(self, outer_locals, used_variables, obj, default_name='unnamed_arg'):
        reversed_named_variables = outer_locals.reverse
        reversed_named_variables.update(used_variables, reverse=True)

        if obj not in reversed_named_variables and is_primitive(obj):
            name = repr(obj)
        else:
            if obj not in reversed_named_variables:
                name = insert_next_available(used_variables, default_name, obj)
            else:
                name = reversed_named_variables[obj]
            reversed_named_variables[obj] = name
            used_variables[name] = obj

        return name

    def find_or_name_args(self, outer_locals, used_variables):
        self.find_or_name_positional_args(outer_locals, used_variables)
        self.find_or_name_kwargs(outer_locals, used_variables)

    def find_or_name_positional_args(self, outer_locals, used_variables):
        for arg in self.call_args:
            recall_arg = self.find_or_name_obj(outer_locals, used_variables, arg)
            self.recall_args.append(recall_arg)

    def find_or_name_kwargs(self, outer_locals, used_variables):
        for key, value in self.call_kwargs.items():
            recall_arg = self.find_or_name_obj(outer_locals, used_variables, value, default_name=key)
            self.recall_kwargs[key] = recall_arg

    def render_recall(self):
        all_args = self.recall_args + [f"{k}={v}" for k, v in self.recall_kwargs.items()]
        call_str = self.fn_name + '(' + ", ".join(all_args) + ')'
        return f'plt.{call_str}'


class SmartPlotContext:
    def __init__(self, save_dir, locals_dict=None, overwrite=False, script_name='make_plot.py'):
        self.save_dir = Path(save_dir)
        self.outer_locals_dict = locals_dict
        self.overwrite = overwrite
        self.regenerate_script_name = script_name

        self.used_variables = {}
        self.calls = []

        if not self.save_dir.exists():
            self.save_dir.mkdir()
        if not self.overwrite and len(list(self.save_dir.glob('*'))) > 0:
            raise Exception(f"Save directory '{self.save_dir.absolute()}' is not empty and overwrite is False")

    def __getattr__(self, fn_name):
        if fn_name in forbidden_plt_fns:
            raise Exception(f'Pyplot function {fn_name} is not allowed in a smartplot context')

        plt_fn = getattr(plt, fn_name)

        @wraps(plt_fn)
        def wrapper(*args, **kwargs):
            ret = plt_fn(*args, **kwargs)
            self.calls.append(Call(
                fn_name,
                args,
                kwargs
            ))
            named_variables = SmartDict(self.outer_locals_dict)
            self.calls[-1].find_or_name_args(named_variables, self.used_variables)
            return ret

        return wrapper

    def save_used_variables(self):
        for var_name, value in self.used_variables.items():
            with open(self.save_dir / f'{var_name}.pkl', 'wb') as f:
                pickle.dump(value, f)

    def save_regenerate_script(self):
        load_variables_code = '\n'.join(
            pickle_load_template.format(var_name=var_name) for var_name in self.used_variables.keys()
        )
        do_plot_code = '\n'.join(call.render_recall() for call in self.calls)

        script_code = script_template.format(
            load_variables_code=load_variables_code,
            do_plot_code=do_plot_code,
        )
        with open(self.save_dir / self.regenerate_script_name, 'w') as f:
            f.write(script_code)

    def save(self):
        self.save_used_variables()
        self.save_regenerate_script()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()
        return False


def load_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    x_data = np.linspace(0, 2 * np.pi, 1000)
    y_data = np.sin(x_data)
    with SmartPlotContext("./data-save-dir", locals(), overwrite=True) as spl:
        spl.plot(x_data, y_data, c='k', label='sin')
        spl.plot(x_data, np.cos(x_data), c='b', label='cos')
        spl.xlabel('xaxis')
        spl.ylabel('yaxis')
        spl.title('Title')
        spl.legend()

        spl.savefig('test.png')
        spl.show()
