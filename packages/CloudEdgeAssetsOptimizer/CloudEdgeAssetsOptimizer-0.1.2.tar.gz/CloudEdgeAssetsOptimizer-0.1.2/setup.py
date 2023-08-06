from setuptools import setup

setup(
    name='CloudEdgeAssetsOptimizer',
    version='0.1.2',
    author='Paulius Tervydis',
    author_email='Paulius.Tervydis@ktu.lt',
    description="""

# CloudEdgeAssetsOptimizer   
    
CloudEdgeAssetsOptimizer is a software tool designed to evaluate and 
optimize the assets within a Cloud and Edge computing network. Its primary 
purpose is to provide insights and estimations to ensure efficient resource
allocation and decision-making. 

The developed software simulates the queues in Cloud and Edge devices, 
providing waiting times, battery consumption of Edge devices, and Servers' 
load. With a fore mentioned parameters available, valuable insights 
for decision-making can be obtained to optimize the network. Alternatively 
automated optimization can be performed using the embedded functions. 
CloudEdgeAssetsOptimizer aims to optimize operational efficiency, 
enhance resource utilization, and ultimately improve overall system 
performance. 

CloudEdgeAssetsOptimizer functions utilize queueing theory principles, 
therefore it also enables users to explore and fine-tune system parameters 
across diverse domains,including telecommunication networks, transportation
and manufacturing systems.

Author: Paulius Tervydis
 
Date: 2023-07-23
""",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pauterv/CloudEdgeAssetsOptimizer',
    packages=['CloudEdgeAssetsOptimizer'],
    install_requires=[
        # List any dependencies your package requires
        'numpy',
        'pandas',
        'matplotlib',
        'Pillow',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
