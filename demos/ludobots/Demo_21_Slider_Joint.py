import sys
sys.path.insert(0, '../..')

import pyrosim
import math


def run(test):

    if test:
        kwargs = {'debug': False, 'play_blind': True, 'eval_time': 500}
    else:
        kwargs = {'debug': True, 'play_blind': False, 'eval_time': 500}

    sim = pyrosim.Simulator(**kwargs)

    ARM_LENGTH = 0.5
    ARM_RADIUS = ARM_LENGTH / 10.0

    cyl1 = sim.send_cylinder(x=0, y=0, z=ARM_LENGTH/2.0 + ARM_RADIUS,
                             r1=0, r2=0, r3=1,
                             length=ARM_LENGTH, radius=ARM_RADIUS)
    cyl2 = sim.send_cylinder(x=0, y=0, z=1.5*ARM_LENGTH,
                             r1=0, r2=0, r3=1,
                             length=ARM_LENGTH, radius=ARM_RADIUS)

    joint = sim.send_slider_joint(first_body_id=cyl1, second_body_id=cyl2,
                                  x=0, y=0, z=1, lo=-.5, hi=.5,
                                  strength=10,
                                  position_control=True)

    touch1 = sim.send_touch_sensor(body_id=cyl1)
    touch2 = sim.send_touch_sensor(body_id=cyl1)

    fneuron = sim.send_function_neuron()

    mneuron = sim.send_motor_neuron(joint_id=joint)

    sim.send_synapse(source_neuron_id=fneuron,
                     target_neuron_id=mneuron, weight=-1.0)

    sim.start()
    sim.wait_to_finish()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run(test=True)
        print('Successfully made slider joint')
    else:
        run(test=False)
