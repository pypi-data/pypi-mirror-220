from distutils.core import setup
setup(
  name = 'buscador',         
  packages = ['buscador'],   
  version = '0.4',      
  license='MIT',        
  description = 'Just a collection of helpful tools',   
  author = 'Samuel Cook',                   
  author_email = 'samcook23@hotmail.com',     
  url = 'https://github.com/SamuelBCook',  
  download_url = 'https://github.com/SamuelBCook/buscador/archive/refs/tags/0.4.tar.gz',    
  keywords = ['tools', 'json', 'easy'],   
  install_requires=[           
          'pandas',
          'boto3',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" 
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.10', 
    'Programming Language :: Python :: 3.9', 
    'Programming Language :: Python :: 3.8',   
  ],
)