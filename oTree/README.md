# Social Value Orientation Task

This is the oTree implementation of the Social Value Orientation Slider Task by Murphy et al. (2014).



#### Setup

copy the application folder to your otree project
add the application to your settings.py file like this

    {
        'name': 'social_value_orientation',
        'display_name': "Social Value Orientation Task",
        'num_demo_participants': 1,
        'app_sequence': ['social_value_orientation'],
    },

otree resetdb

* Run the below command to run the server on port 3000 on all of the interfaces
otree runserver 0.0.0.0:3000


#### Requirement
* otree>3.0.0
