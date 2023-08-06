import yaml

import catmux.session

def test_debug_split():
    split_data = {"commands": ["echo 'hello'"]}
    split = catmux.split.Split(**split_data)
    split.debug (name="test_split", prefix="")

def test_debug():
    CONFIG = """common:
    before_commands:
        - echo "hello"
        - echo "world"
    default_window: foobar
windows:
    - name: left-right
      splits:
        - commands:
          - echo "left"
    - name: foo
      splits:
        - commands:
          - echo "left"
"""
    session = catmux.session.Session("server", "name")
    session.init_from_yaml(yaml.safe_load(CONFIG))
    session._windows[0].debug()

