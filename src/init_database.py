from database_connection import get_database_connection


def drop_tables(connection):
    """Delete existing database tables before creating new ones."""
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS sudokus")
    cursor.execute("DROP TABLE IF EXISTS stats")

    connection.commit()


def create_tables(connection):
    """Create tables for the database."""
    cursor = connection.cursor()

    cursor.execute(
        """CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)"""
    )
    cursor.execute(
        """CREATE TABLE sudokus (id INTEGER PRIMARY KEY, name TEXT UNIQUE,
        puzzle TEXT UNIQUE, level INTEGER)"""
    )
    cursor.execute(
        """CREATE TABLE stats (id INTEGER PRIMARY KEY, user_id REFERENCES users,
        sudoku_id REFERENCES sudokus, playtime INTEGER)"""
    )

    connection.commit()


def create_easy_sudokus(connection):
    """Create easy starting sudokus."""
    cursor = connection.cursor()

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("easy1", 
        "000000478050940030600800901305400000000010062126000040003009125269005704000270000", 1)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("easy2", 
        "009010000872906405160074008950000060021050900704369500300005200200001050000603100", 1)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("easy3", 
        "75962000401604000000000590060100400000071304608006209000020800300000650198056070", 1)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("easy4", 
        "050901200700000000023700840090250030375080000000004975000890000549100000138546020", 1)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("easy5", 
        "057006023010300000000102078002000840030400500605901030001600350003010090064230080", 1)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("easy6", 
        "802107453001040906004308070600800300100429000500000000210006507075080030000000002", 1)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("easy7", 
        "208750900506900810000640072904830627700400150000010009003176000000000706050000000", 1)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("easy8", 
        "001050200006700904894026000000240007900610043003090620060070080179080450300009000", 1)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("easy9", 
        "000870000047006281000200390080020710950003862100008030090060000005100000416000020", 1)"""
    )

    connection.commit()


def create_medium_sudokus(connection):
    """Create medium level sudokus."""

    cursor = connection.cursor()

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("medium1", 
        "100020058960100007028640000000000000005002013007390006032800000700400862800000405", 2)"""
    )
    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("medium2", 
        "190000004002100000074398000009000258040000000001005079200703000400800600008062703", 2)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("medium3", 
        "000706000400000702057090106040010080000300005000007200006030009030040010010975600", 2)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("medium4", 
        "000090000070000082080000406800000600167000000940106820026001000503008004008600135", 2)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("medium5", 
        "080506200000090340309200001000010060603020090120709004004070018210600000000000407", 2)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("medium6", 
        "309108000000795300000600790057210000000000000436509007000001400600057930900020006", 2)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("medium7", 
        "071040000090100500030090618040200080200009000009000020008430000503600900760000003", 2)"""
    )

    connection.commit()


def create_hard_sudokus(connection):
    """Create hard level sudokus."""
    cursor = connection.cursor()

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("hard1", 
        "070003000000007060603000082200400306000816504000200000004058070086700000005060100", 3)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("hard2", 
        "008000709000006208470200000035700010000000060000040002900000000500430800604000020", 3)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("hard3", 
        "500000000009000004010300070000000800200057060670400000038000005000004010007508200", 3)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("hard4", 
        "000050209900000000040003000000670010080000020050800697470001000600780001501000408", 3)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("hard5", 
        "401006000000050000080000500000067100000320040073001080107900000040000008600000420", 3)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("hard6", 
        "000004800003500001000000750100000000006300045000002006090060000030090072470010003", 3)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("hard7", 
        "050000049041600000030007500000060200800001000100200006000740650400000000000030002", 3)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("hard8", 
        "200000400003900010008000750030160000050080097100004000012007003000000000000300600", 3)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("hard9", 
        "000200000000070300000089001800020050000107004106000000080000510230004900000790020", 3)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("very hard", 
        "094000000000000465300072000172040090008000000009000300060100050200300006000080007", 3)"""
    )

    cursor.execute(
        """INSERT INTO sudokus (name, puzzle, level) values ("really hard", 
        "900800200001050007000070030005000000020300400300200000008000650490000000000064001", 3)"""
    )

    connection.commit()


def init_db():
    """Initialize the database and it's content."""
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)
    create_easy_sudokus(connection)
    create_medium_sudokus(connection)
    create_hard_sudokus(connection)


if __name__ == "__main__":
    init_db()
