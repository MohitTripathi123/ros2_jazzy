"""Check model, bridge and navigation contracts without a physics server."""

import ast
import itertools
import math
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

import pytest
import xacro
import yaml


PACKAGE = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def robot():
    return ET.fromstring(xacro.process_file(
        str(PACKAGE / 'urdf/simple_robot.xacro')).toxml())


def launch_strings():
    tree = ast.parse((PACKAGE / 'launch/gazebo_robot.launch.py').read_text())
    return {node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)}


def test_drive_geometry_and_bridge(robot):
    drive = robot.find(".//plugin[@name='gz::sim::systems::DiffDrive']")
    assert drive.find('cmd_vel_topic') is None
    assert drive.findtext('topic') == '/cmd_vel'
    assert '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist' in launch_strings()
    origins = []
    for side in ('left', 'right'):
        joint = robot.find(f"joint[@name='{drive.findtext(side + '_joint')}']")
        origins.append(float(joint.find('origin').get('xyz').split()[1]))
        link = robot.find(f"link[@name='{joint.find('child').get('link')}']")
        wheel = link.find('collision/geometry/cylinder')
        assert float(drive.findtext('wheel_radius')) == float(wheel.get('radius'))
    assert float(drive.findtext('wheel_separation')) == pytest.approx(
        abs(origins[0] - origins[1]))
    assert drive.findtext('frame_id') == 'odom'
    assert drive.findtext('child_frame_id') == 'base_link'
    assert drive.findtext('odom_topic') == '/odom'


def test_sensor_bridge_topics(robot):
    strings = launch_strings()
    camera = robot.find(".//sensor[@type='camera']")
    assert camera.findtext('topic') + '@sensor_msgs/msg/Image[gz.msgs.Image' in strings
    info = camera.findtext('camera/camera_info_topic')
    assert info + '@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo' in strings
    lidar = robot.find(".//sensor[@type='gpu_lidar']")
    assert ('/' + lidar.findtext('topic').lstrip('/') +
            '@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan') in strings


def collision_radius(robot):
    """Bound collision geometry in XY, including rotated wheel cylinders."""
    required = 0.0
    for link in robot.findall('link'):
        for collision in link.findall('collision'):
            # All collision-bearing links attach directly to base_link in this model.
            joint = next((j for j in robot.findall('joint')
                          if j.find('child').get('link') == link.get('name')), None)
            xyz = [0.0, 0.0, 0.0]
            if joint is not None:
                assert joint.find('parent').get('link') == 'base_link'
                assert joint.find('origin').get('rpy', '0 0 0') == '0 0 0'
                xyz = list(map(float, joint.find('origin').get('xyz').split()))
            origin = collision.find('origin')
            roll = 0.0
            if origin is not None:
                offset = list(map(float, origin.get('xyz', '0 0 0').split()))
                xyz = [a + b for a, b in zip(xyz, offset)]
                roll, pitch, yaw = map(float, origin.get('rpy', '0 0 0').split())
                assert pitch == yaw == 0.0
            shape = list(collision.find('geometry'))[0]
            if shape.tag == 'sphere':
                required = max(required, math.hypot(*xyz[:2]) + float(shape.get('radius')))
                continue
            if shape.tag == 'box':
                half = [float(v) / 2 for v in shape.get('size').split()]
            else:
                assert shape.tag == 'cylinder'
                half = [float(shape.get('radius'))] * 2 + [float(shape.get('length')) / 2]
            for signs in itertools.product((-1, 1), repeat=3):
                x, y, z = [a * b for a, b in zip(half, signs)]
                y_rotated = y * math.cos(roll) - z * math.sin(roll)
                required = max(required, math.hypot(xyz[0] + x, xyz[1] + y_rotated))
    return required


def test_costmap_radius_contains_model(robot):
    params = yaml.safe_load((PACKAGE / 'config/nav2_params.yaml').read_text())
    required = collision_radius(robot)
    radii = []
    for name, frame in (('local_costmap', 'odom'), ('global_costmap', 'map')):
        config = params[name][name]['ros__parameters']
        assert config['robot_base_frame'] == 'base_link'
        assert config['global_frame'] == frame
        assert not config.get('footprint')  # An explicit footprint overrides the radius.
        radii.append(config['robot_radius'])
        assert config['robot_radius'] >= required
        assert config['inflation_layer']['inflation_radius'] >= config['robot_radius']
    assert radii[0] == radii[1]
    assert params['amcl']['ros__parameters']['base_frame_id'] == 'base_link'
    assert params['amcl']['ros__parameters']['odom_frame_id'] == 'odom'


def test_sdf_preserves_drive_and_sensor_contract(robot, tmp_path):
    urdf = tmp_path / 'robot.urdf'
    ET.ElementTree(robot).write(urdf, encoding='unicode')
    result = subprocess.run(['gz', 'sdf', '-p', str(urdf)],
                            check=True, capture_output=True, text=True)
    sdf = ET.fromstring(result.stdout)
    drive = sdf.find(".//plugin[@name='gz::sim::systems::DiffDrive']")
    assert drive.findtext('topic') == '/cmd_vel'
    assert float(drive.findtext('wheel_separation')) == pytest.approx(0.45)
    assert sdf.findtext('.//camera/camera_info_topic') == '/camera/camera_info'


def test_documented_nav2_booleans():
    document = (PACKAGE.parents[1] / 'course_lectures' /
                'applied-practical-checkpoints.md').read_text()
    assert 'use_composition:=false' not in document
    assert '  slam:=false map:=' not in document
    assert document.count('use_composition:=False') >= 2
    assert 'slam:=False map:=' in document
    assert 'use_slam:=false' in document
