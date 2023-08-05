"""Tests the yaml constructors"""
import io
import operator
import os

import numpy as np
import pytest
import ruamel.yaml

from yayaml import ConstructorError, RepresenterError, load_yml, yaml

# Fixtures --------------------------------------------------------------------


@pytest.fixture()
def yamlstrs() -> dict:
    """Prepares a list of yaml strings to test against"""
    # NOTE Leading indentation is ignored by yaml
    strs = {
        "slice": """
            slices:
             - !slice 5
             - !slice [5]
             - !slice [0, ~]
             - !slice [~, 0]
             - !slice [0, 10, 2]
             - !slice [0, 10, None]
             - !slice [2, None, 2]
        """,
        "range": """
            ranges:
             - !range 10
             - !range [10]
             - !range [5, 10]
             - !range [5, 10, 2]
        """,
        "listgen": """
            lists:
             - !listgen [10]
             - !listgen [0, 10, 2]
             - !listgen
               from_range: [0, 10, 3]
               unique: true
               append: [100]
               remove: [0]
               sort: true
             - !listgen [5, 10, 2]
        """,
        "copy": """
            copy:
              foo: !deepcopy &foo
                bar: baz
              foo2:
                <<: *foo
              seq: !deepcopy
               - 1
               - 2
              scalar: !deepcopy 123
        """,
        "utils": """
            utils:
              # START -- utility-yaml-tags
              any:      !any        [false, 0, true]    # == True
              all:      !all        [true, 5, 0]        # == False

              abs:      !abs        -1          # +1
              int:      !int        1.23        # 1
              round:    !round      9.87        # 10
              sum:      !sum        [1, 2, 3]   # 6
              prod:     !prod       [2, 3, 4]   # 24

              min:      !min        [1, 2, 3]   # 1
              max:      !max        [1, 2, 3]   # 3

              sorted:   !sorted     [2, 1, 3]   # [1, 2, 3]
              isorted:  !isorted    [2, 1, 3]   # [3, 2, 1]

              # Operators
              add:      !add        [1, 2]      # 1 + 2
              sub:      !sub        [2, 1]      # 2 - 1
              mul:      !mul        [3, 4]      # 3 * 4
              mod:      !mod        [3, 2]      # 3 % 2
              pow:      !pow        [2, 4]      # 2 ** 4
              truediv:  !truediv    [3, 2]      # 3 / 2
              floordiv: !floordiv   [3, 2]      # 3 // 2
              pow_mod:  !pow        [2, 4, 3]   # 2 ** 4 % 3

              not:      !not        [true]
              and:      !and        [true, false]
              or:       !or         [true, false]
              xor:      !xor        [true, true]

              lt:       !lt         [1, 2]      # 1 <  2
              le:       !le         [2, 2]      # 2 <= 2
              eq:       !eq         [3, 3]      # 3 == 3
              ne:       !ne         [3, 1]      # 3 != 1
              ge:       !ge         [2, 2]      # 2 >= 2
              gt:       !gt         [4, 3]      # 4 >  3

              negate:   !negate     [1]             # -1
              invert:   !invert     [true]          # ~true
              contains: !contains   [[1,2,3], 4]    # 4 in [1,2,3] == False

              concat:   !concat     [[1,2,3], [4,5], [6,7,8]]  # […]+[…]+[…]+…

              # List generation
              # ... using the paramspace.tools.create_indices function
              list1:    !listgen    [0, 10, 2]   # [0, 2, 4, 6, 8]
              list2:    !listgen
                from_range: [0, 10, 3]
                unique: true
                append: [100]
                remove: [0]
                sort: true

              # ... using np.linspace, np.logspace, np.arange
              lin:      !linspace   [-1, 1, 5]   # [-1., -.5, 0., .5, 1.]
              log:      !logspace   [1, 4, 4]    # [10., 100., 1000., 10000.]
              arange:   !arange     [0, 1, .2]   # [0., .2, .4, .6, .8]

              # String formatting
              format1:  !format     ["{} is not {}", foo, bar]
              format2:  !format
                fstr: "{some_key:}: {some_value:}"
                some_key: fish
                some_value: spam
              format3:  !format
                fstr: "results: {stats[mean]:.2f} ± {stats[std]:.2f}"
                stats:
                  mean: 1.632
                  std:  0.026

              # Joining and splitting strings
              joined_words: !join    # -> "foo | bar | baz"
                - " | "
                - [foo, bar, baz]

              words: !split          # -> [there, are, many, words, in this, sentence]
                - there are many words in this sentence
                - " "
                # - 3                # optional `maxsplit` argument
              # END ---- utility-yaml-tags


              # NOTE Need to choose env. variables that are available in CI
              # START -- envvars-and-path-handling
              # Reading environment variables, optionally with fallback
              PATH:             !getenv PATH   # fails if variable is missing
              username:         !getenv [USER, "unknown_user"]
              home_directory:   !getenv [HOME, "/"]

              # Expanding a path containing `~`
              some_user_path:   !expanduser ~/some/path

              # Joining paths
              some_joined_path: !joinpath      # -> "~/foo/bar/../spam.txt"
                - "~"
                - foo
                - bar
                - ..
                - spam.txt
              # END ---- envvars-and-path-handling

              # More tests that don't need to be part of the docs
              pow_mod2: !pow {x: 2, y: 4, z: 3}
        """,
        #
        # Failing or warning cases
        ("_listgen_scalar", TypeError): "string_node: !listgen foo",
    }

    return strs


# -- Tests --------------------------------------------------------------------
# .. Legacy tests (not easy to extend) ........................................
# TODO Rewrite these


def test_load_and_safe(yamlstrs):
    """Tests whether the constructor and representers work"""
    # Test plain loading
    for name, ystr in yamlstrs.items():
        print("\n\nName of yamlstr that will be loaded: ", name)

        if isinstance(name, tuple):
            # Expected to warn or raise
            if len(name) == 2:
                name, exc = name
                warn = None
            elif len(name) == 3:
                name, exc, warn = name

            # Distinguish three cases
            if warn and exc:
                with pytest.raises(exc):
                    with pytest.warns(warn):
                        yaml.load(ystr)

            elif warn and not exc:
                with pytest.warns(warn):
                    yaml.load(ystr)

            elif exc and not warn:
                with pytest.raises(exc):
                    yaml.load(ystr)

            continue

        # else: Expected to load correctly
        obj = yaml.load(ystr)

        # Test the representer runs through
        stream = io.StringIO("")
        yaml.dump(obj, stream=stream)
        output = "\n".join(stream.readlines())

        # TODO Test output


def test_correctness(yamlstrs):
    """Tests the correctness of the constructors"""
    res = {}

    # Load the resolved yaml strings
    for name, ystr in yamlstrs.items():
        print("Name of yamlstr that will be loaded: ", name)
        if isinstance(name, tuple):
            # Will fail, don't use
            continue
        res[name] = yaml.load(ystr)

    # Test the utility constructors
    utils = res["utils"]["utils"]
    assert utils["any"] == any([False, 0, True])
    assert utils["all"] == all([True, 5, 0])
    assert utils["abs"] == abs(-1)
    assert utils["int"] == int(1.23)
    assert utils["round"] == round(9.87) == 10
    assert utils["min"] == min([1, 2, 3])
    assert utils["max"] == max([1, 2, 3])
    assert utils["sorted"] == sorted([2, 1, 3])
    assert utils["isorted"] == sorted([2, 1, 3], reverse=True)
    assert utils["sum"] == sum([1, 2, 3])
    assert utils["prod"] == 2 * 3 * 4
    assert utils["add"] == operator.add(*[1, 2])
    assert utils["sub"] == operator.sub(*[2, 1])
    assert utils["mul"] == operator.mul(*[3, 4])
    assert utils["truediv"] == operator.truediv(*[3, 2])
    assert utils["floordiv"] == operator.floordiv(*[3, 2])
    assert utils["mod"] == operator.mod(*[3, 2])
    assert utils["pow"] == 2**4
    assert utils["pow_mod"] == 2**4 % 3 == pow(2, 4, 3)
    assert utils["pow_mod2"] == 2**4 % 3 == pow(2, 4, 3)
    assert utils["not"] == operator.not_(*[True])
    assert utils["and"] == operator.and_(*[True, False])
    assert utils["or"] == operator.or_(*[True, False])
    assert utils["xor"] == operator.xor(*[True, True])
    assert utils["lt"] == operator.lt(*[1, 2])
    assert utils["le"] == operator.le(*[2, 2])
    assert utils["eq"] == operator.eq(*[3, 3])
    assert utils["ne"] == operator.ne(*[3, 1])
    assert utils["ge"] == operator.ge(*[2, 2])
    assert utils["gt"] == operator.gt(*[4, 3])
    assert utils["negate"] == operator.neg(*[1])
    assert utils["invert"] == operator.invert(*[True])
    assert utils["contains"] == operator.contains(*[[1, 2, 3], 4])
    assert utils["concat"] == [1, 2, 3] + [4, 5] + [6, 7, 8]
    assert utils["format1"] == "foo is not bar"
    assert utils["format2"] == "fish: spam"
    assert utils["format3"] == "results: 1.63 ± 0.03"
    assert utils["joined_words"] == "foo | bar | baz"
    assert utils["words"] == [
        "there",
        "are",
        "many",
        "words",
        "in",
        "this",
        "sentence",
    ]

    assert utils["list1"] == [0, 2, 4, 6, 8]
    assert utils["list2"] == [3, 6, 9, 100]
    assert utils["lin"] == [-1.0, -0.5, 0.0, 0.5, 1.0]
    assert utils["log"] == [10.0, 100.0, 1000.0, 10000.0]
    assert np.isclose(utils["arange"], [0.0, 0.2, 0.4, 0.6, 0.8]).all()

    assert utils["some_user_path"] == os.path.expanduser("~/some/path")

    assert utils["PATH"] == os.environ["PATH"]
    assert utils["username"] == os.environ.get("USER", "unknown_user")
    assert utils["home_directory"] == os.environ.get("HOME", "/")


# -- Newer tests --------------------------------------------------------------
# .. Representation ...........................................................


def test_represent_custom_class():
    from collections import namedtuple

    from yayaml import add_representer, build_representer, yaml_dumps

    Point = namedtuple("Point", ["x", "y"])
    pt = Point(123, 234)

    # FIXME This somehow breaks yaml_dumps
    # with pytest.raises(RepresenterError, match="Could not serialize"):
    #     yaml_dumps(pt)

    # Register the representer
    add_representer(
        Point,
        build_representer(lambda pt: dict(x=pt.x, y=pt.y)),
    )

    # This should work now
    assert "123" in yaml_dumps(dict(pt=pt))

    # How about some type that can be represented as a scalar
    MyInt = namedtuple("MyInt", ["value"])
    my_int = MyInt(123)

    # FIXME This somehow breaks yaml_dumps
    # with pytest.raises(RepresenterError, match="Could not serialize"):
    #     yaml_dumps(my_int)

    add_representer(
        MyInt,
        build_representer(lambda my_int: my_int.value),
    )

    assert "123" in yaml_dumps(my_int)


def test_representer_decorator():
    from collections import namedtuple

    from yayaml import build_representer, is_representer, yaml_dumps

    Point = namedtuple("Point", ["x", "y"])

    @is_representer(Point)
    def represent_point(r, pt, *, tag: str):
        return r.represent_sequence(tag, [pt.x, pt.y])

    pt = Point(123, 234)
    assert "123" in yaml_dumps(dict(pt=pt))


# .. Construction .............................................................


def test_construction_error_messages():
    # For function-based constructors, information is added
    with pytest.raises(
        ruamel.yaml.constructor.ConstructorError, match="expected at most 3"
    ):
        yaml.load("!range [1,2,3,4]")


def test_scalar_node_construction():
    assert yaml.load("!deepcopy 1") == 1
    assert yaml.load("!deepcopy 1.2") == 1.2
    assert yaml.load("!deepcopy inf") == float("inf")
    assert yaml.load("!deepcopy some string") == "some string"

    assert yaml.load("!deepcopy false") is False
    assert yaml.load("!deepcopy no") is False

    assert yaml.load("!deepcopy ~") is None
    assert yaml.load("!deepcopy null") is None


def test_expr_constructor():
    """Tests the expression constructor"""
    tstr = """
        one:   !expr 1*2*3
        two:   !expr 9 / 2
        three: !expr 2**4
        four:  !expr 1e-10
        five:  !expr 1E10
        six:   !expr inf
        seven: !expr NaN
        eight: !expr (2 + 3) * 4
        nine:  !expr -inf
    """

    # Load the string using the tools module, where the constructor was added
    d = yaml.load(tstr)

    # Assert correctness
    assert d["one"] == 1 * 2 * 3
    assert d["two"] == 9 / 2
    assert d["three"] == 2**4
    assert d["four"] == eval("1e-10") == 10.0 ** (-10)
    assert d["five"] == eval("1E10") == 10.0**10
    assert d["six"] == np.inf
    assert np.isnan(d["seven"])
    assert d["eight"] == (2 + 3) * 4
