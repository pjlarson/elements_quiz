"""Periodic table data with all 118 elements."""

# List of all elements: (atomic_number, symbol, name, valence_electrons, discovery_year)
ELEMENTS = [
    (1, "H", "Hydrogen", 1, 1766),
    (2, "He", "Helium", 2, 1868),
    (3, "Li", "Lithium", 1, 1817),
    (4, "Be", "Beryllium", 2, 1798),
    (5, "B", "Boron", 3, 1808),
    (6, "C", "Carbon", 4, "ancient"),
    (7, "N", "Nitrogen", 5, 1772),
    (8, "O", "Oxygen", 6, 1774),
    (9, "F", "Fluorine", 7, 1886),
    (10, "Ne", "Neon", 8, 1898),
    (11, "Na", "Sodium", 1, 1807),
    (12, "Mg", "Magnesium", 2, 1755),
    (13, "Al", "Aluminum", 3, 1825),
    (14, "Si", "Silicon", 4, 1824),
    (15, "P", "Phosphorus", 5, 1669),
    (16, "S", "Sulfur", 6, "ancient"),
    (17, "Cl", "Chlorine", 7, 1774),
    (18, "Ar", "Argon", 8, 1894),
    (19, "K", "Potassium", 1, 1807),
    (20, "Ca", "Calcium", 2, 1808),
    (21, "Sc", "Scandium", 2, 1879),
    (22, "Ti", "Titanium", 2, 1791),
    (23, "V", "Vanadium", 2, 1801),
    (24, "Cr", "Chromium", 1, 1797),
    (25, "Mn", "Manganese", 2, 1774),
    (26, "Fe", "Iron", 2, "ancient"),
    (27, "Co", "Cobalt", 2, 1735),
    (28, "Ni", "Nickel", 2, 1751),
    (29, "Cu", "Copper", 1, "ancient"),
    (30, "Zn", "Zinc", 2, "ancient"),
    (31, "Ga", "Gallium", 3, 1875),
    (32, "Ge", "Germanium", 4, 1886),
    (33, "As", "Arsenic", 5, "ancient"),
    (34, "Se", "Selenium", 6, 1817),
    (35, "Br", "Bromine", 7, 1826),
    (36, "Kr", "Krypton", 8, 1898),
    (37, "Rb", "Rubidium", 1, 1861),
    (38, "Sr", "Strontium", 2, 1790),
    (39, "Y", "Yttrium", 2, 1794),
    (40, "Zr", "Zirconium", 2, 1789),
    (41, "Nb", "Niobium", 1, 1801),
    (42, "Mo", "Molybdenum", 1, 1781),
    (43, "Tc", "Technetium", 2, 1937),
    (44, "Ru", "Ruthenium", 1, 1844),
    (45, "Rh", "Rhodium", 1, 1803),
    (46, "Pd", "Palladium", 0, 1803),
    (47, "Ag", "Silver", 1, "ancient"),
    (48, "Cd", "Cadmium", 2, 1817),
    (49, "In", "Indium", 3, 1863),
    (50, "Sn", "Tin", 4, "ancient"),
    (51, "Sb", "Antimony", 5, "ancient"),
    (52, "Te", "Tellurium", 6, 1782),
    (53, "I", "Iodine", 7, 1811),
    (54, "Xe", "Xenon", 8, 1898),
    (55, "Cs", "Cesium", 1, 1860),
    (56, "Ba", "Barium", 2, 1808),
    (57, "La", "Lanthanum", 2, 1839),
    (58, "Ce", "Cerium", 2, 1803),
    (59, "Pr", "Praseodymium", 2, 1885),
    (60, "Nd", "Neodymium", 2, 1885),
    (61, "Pm", "Promethium", 2, 1945),
    (62, "Sm", "Samarium", 2, 1879),
    (63, "Eu", "Europium", 2, 1901),
    (64, "Gd", "Gadolinium", 2, 1880),
    (65, "Tb", "Terbium", 2, 1843),
    (66, "Dy", "Dysprosium", 2, 1886),
    (67, "Ho", "Holmium", 2, 1878),
    (68, "Er", "Erbium", 2, 1843),
    (69, "Tm", "Thulium", 2, 1879),
    (70, "Yb", "Ytterbium", 2, 1878),
    (71, "Lu", "Lutetium", 2, 1907),
    (72, "Hf", "Hafnium", 2, 1923),
    (73, "Ta", "Tantalum", 2, 1802),
    (74, "W", "Tungsten", 2, 1783),
    (75, "Re", "Rhenium", 2, 1925),
    (76, "Os", "Osmium", 2, 1803),
    (77, "Ir", "Iridium", 2, 1803),
    (78, "Pt", "Platinum", 1, 1735),
    (79, "Au", "Gold", 1, "ancient"),
    (80, "Hg", "Mercury", 2, "ancient"),
    (81, "Tl", "Thallium", 3, 1861),
    (82, "Pb", "Lead", 4, "ancient"),
    (83, "Bi", "Bismuth", 5, "ancient"),
    (84, "Po", "Polonium", 6, 1898),
    (85, "At", "Astatine", 7, 1940),
    (86, "Rn", "Radon", 8, 1900),
    (87, "Fr", "Francium", 1, 1939),
    (88, "Ra", "Radium", 2, 1898),
    (89, "Ac", "Actinium", 2, 1899),
    (90, "Th", "Thorium", 2, 1829),
    (91, "Pa", "Protactinium", 2, 1913),
    (92, "U", "Uranium", 2, 1789),
    (93, "Np", "Neptunium", 2, 1940),
    (94, "Pu", "Plutonium", 2, 1940),
    (95, "Am", "Americium", 2, 1944),
    (96, "Cm", "Curium", 2, 1944),
    (97, "Bk", "Berkelium", 2, 1949),
    (98, "Cf", "Californium", 2, 1950),
    (99, "Es", "Einsteinium", 2, 1952),
    (100, "Fm", "Fermium", 2, 1952),
    (101, "Md", "Mendelevium", 2, 1955),
    (102, "No", "Nobelium", 2, 1958),
    (103, "Lr", "Lawrencium", 3, 1961),
    (104, "Rf", "Rutherfordium", 2, 1969),
    (105, "Db", "Dubnium", 2, 1970),
    (106, "Sg", "Seaborgium", 2, 1974),
    (107, "Bh", "Bohrium", 2, 1981),
    (108, "Hs", "Hassium", 2, 1984),
    (109, "Mt", "Meitnerium", 2, 1982),
    (110, "Ds", "Darmstadtium", 2, 1994),
    (111, "Rg", "Roentgenium", 2, 1994),
    (112, "Cn", "Copernicium", 2, 1996),
    (113, "Nh", "Nihonium", 3, 2003),
    (114, "Fl", "Flerovium", 4, 1999),
    (115, "Mc", "Moscovium", 5, 2003),
    (116, "Lv", "Livermorium", 6, 2000),
    (117, "Ts", "Tennessine", 7, 2010),
    (118, "Og", "Oganesson", 8, 2006),
]


def get_element_by_number(atomic_number: int) -> tuple:
    """Get element tuple by atomic number."""
    for element in ELEMENTS:
        if element[0] == atomic_number:
            return element
    return None


def get_element_by_symbol(symbol: str) -> tuple:
    """Get element tuple by symbol (case-insensitive)."""
    symbol = symbol.strip()
    for element in ELEMENTS:
        if element[1].lower() == symbol.lower():
            return element
    return None


def get_element_by_name(name: str) -> tuple:
    """Get element tuple by name (case-insensitive)."""
    name = name.strip()
    for element in ELEMENTS:
        if element[2].lower() == name.lower():
            return element
    return None
