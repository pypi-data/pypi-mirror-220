from distutils.core import setup
setup(
  name = 'buscador',         
  packages = ['buscador'],   
  version = '0.1',      
  license='MIT',        
  description = 'Just a collection of helpful tools',   
  author = 'Samuel Cook',                   
  author_email = 'samcook23@hotmail.com',     
  url = 'https://github.com/SamuelBCook',  
  download_url = 'https://github.com/SamuelBCook/buscador/archive/refs/tags/0.1.tar.gz',    # I explain this later on
  keywords = ['tools', 'json', 'easy'],   
  install_requires=[            # I get to this in a second
          'pandas',
          'json',
          'time',
          'boto3'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" 
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.11',    
  ],
)