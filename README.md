#Minify - JS and CSS minification on the fly

__Author__  - Harshita Kasera

__License__ - GPLv2/MIT


#Introduction
A python script to minify jss and css files on the fly using yui compressor

#Usage
<pre>minify.py [-h] [--all | --js | --css | --clear]</pre>

Optional Arguments :
<pre>
 -h, --help   :   Show help message and exit
 --all        :   Minify all js and css files
 --js         :   Minify only js files
 --css        :   Minify only css files
 --clear      :   Clear all minified files
</pre>

<pre>$> python minify.py --all</pre>

#Output 
![Sample output](https://raw.github.com/hkasera/minify/master/help/Output.png "Sample Output")

#Version History

__1.0.0__
Initial Release
