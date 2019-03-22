# event loop
# https://github.com/harvimt/quamash
# an asyncio eventloop for PyQt.
from quamash import QEventLoop
import asyncio
from PyQt5.QtWidgets import QApplication
from widgets.main import Main
from service.util import open_session,close_session

if __name__ == "__main__":
    """
    在PyQt5中,如果在Python 代码中抛出了异常,没有进行捕获,异常只要进入事件循环,程序就崩溃,而没有任何提示,给程序调试带来不少麻烦,通过在程序运行前加入以下代码,则能避免程序崩溃.
    import cgitb 
    cgitb.enable( format = ‘text’)
    """
    import sys
    import qdarkstyle
    import cgitb
    cgitb.enable(format='text')#
    app = QApplication(sys.argv)
    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        Form = Main()
        loop.run_until_complete(open_session())
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        Form.initUI()
        Form.resize(1022, 700)
        #Form.resize(600, 400)
        Form.show()
        #sys.exit(app.exec_())
        loop.run_forever()
        loop.run_until_complete(close_session())
        #print("close")