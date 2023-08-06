from setuptools import setup

setup(name='aggdirect_job_report_utility',
      packages=['aggdirect_job_report_utility'],
      version='0.0.8',
      description='Job report utility functions',
      # url='http://github.com/storborg/funnyone',
      author='Chinmoy Das',
      # author_email='cdchinmoy@gmail.com',
      license='MIT',
      zip_safe=False,
      keywords = ['aggdirect', 'job_report', 'job_report_utility'],
      install_requires=[ 
            'pandas',
            'numpy',
            ],
      classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
      ],)