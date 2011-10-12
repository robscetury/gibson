__author__ = 'rob'

from distutils.core import setup
from distutils.extension import Extension

setup(
    ext_modules= [Extension("gibson.physics.spring", "gibson/physics/spring.pyx")]
)