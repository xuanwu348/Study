from app import app
import sys

if sys.version_info.major != 3:
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0")
