import controller
import psycopg2

c = controller.Controller()
if not c.OpenBD(5432) == -1:
    c.start()
    try:
        c.CloseBD()
    except psycopg2.InterfaceError:
        do_nothing = 0
