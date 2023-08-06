<h1 align="center"> <a href="https://imgur.com/L01ipPl"><img src="https://i.imgur.com/L01ipPl.png" title="source: imgur.com" /></a>
  
<h1 align="center"> PySolidState (PySS) </h1>

>PySS es una biblioteca desarrollada como una herramienta de apoyo para el estudio introductorio del estado sólido y los conceptos básicos de los materiales. Su enfoque principal es proporcionar apoyo visual y funcionalidades que permitan asentar los conceptos fundamentales en esta área de estudio, desde estructuras cristalinas hasta modelos de enlace fuerte. Con un conjunto de herramientas y funcionalidades, PySolidState permite a investigadores y estudiantes analizar y simular varios aspectos de la física del estado sólido. Además, esta biblioteca se combina con notas de curso sobre estado sólido, lo que la convierte en un recurso bastante completo para el aprendizaje de la materia a nivel universitario. Gracias a su enfoque en la visualización y el apoyo práctico, PySolidState se convierte en una valiosa herramienta que, junto con las notas de curso, ofrece una base sólida para comprender los principios y fundamentos del estado sólido.

**Deployment**

![PyPI](https://img.shields.io/pypi/v/PySolidState)

## Recursos
- Documentación
- Notas del curso de estado solido

## Instalación
Se recomienda utilizar pip para la instalación. Asegúrese de que la última versión esté instalada, ya que PySS se actualiza con frecuencia:

>Nota: Es importante antes de instalar la libreria PySolidState haber ejecutado la consola en modo administrador si se trabajara con jupyter notebook.

ejecute los siguientes comando para la instalación:
```python
   pip install PySolidState    # Instalacion normal
   pip install --upgrade PySolidState  # o actualizar si es necesario
```
**Dependencias Requeridas:**
- Python 3.9+
- matplotlib >=3.7.1
- numpy>=1.24.3
- mayavi>=4.7.2
- scikit-spatial>=7.0.0

## Uso
### Crear Red (Create Lattice):
Uno de los conceptos mas basico y fundamental en el estado solido es el de red, siendo las unicas posibles en formar estructuras cistalinas las redes de Bravais; para crea una de estas tenemos dos formas de hacerlo:

**1)** Construyendo la red a partir de los parámetros ***System*** (nombre de una de las redes de Brabais),  ***structure_type*** (Si la red tiene centrada en las caras, centrada en el cuerpo o centrada en las bases) y ***dimension*** (dimensión en la cual se creara la red 2D o 3D). A continuación se muestra un ejemplo de uso:
```python
from PySolidState.crystal_structure.lattice import Lattice  # Importamos el modulo estructura cristalina de la libreria junto al metodo lattices

lattice = Lattice(system='cubic',structure_type='face_centered', dimension='3D') # Se crea la red
lattice.plot()  # Se grafica la red
```
**2)** Construyendo la red a partir de los parámetros ***magnitude*** (tupla con la norma de cada uno de los vectores de la red a1, a2 y a3),  ***angles*** (tupla con los angulos que describen los vectores de la red (Gama, Alfa, Beta)) y ***dimension*** (dimensión en la cual se creara la red 2D o 3D). A continuación se muestra un ejemplo de uso:
```python
from PySolidState.crystal_structure.lattice import Lattice  # Importamos el modulo estructura cristalina de la libreria junto al metodo lattices

lattice = Lattice(magnitude=(1,1,1),angles=(90,90,90), dimension='3D') # Se crea la red
lattice.plot()  # Se grafica la red
```
### Crear base (Create base):
El otro concepto más básico es el de base, siendo esta base el conjunto de átomos que se acomodan en cada punto de red para formar la estructura cristalina. A continuación se muestra un ejemplo de como crear esta base de átomos:

```python
# Se importan los módulos Lattice, Atom, Base
from PySolidState.crystal_structure.lattice import Lattice
from PySolidState.crystal_structure.atom import Atom
from PySolidState.crystal_structure.base import Base

#Se crean los átomos que harán parte de la base de átomos
atom2 = Atom(name='Na+', size= 0.2, color= 'orangered')
atom1 = Atom(name='Cl-', size= 0.3, color= 'springgreen')

#Se crea la red a la cual se acomodaran
lattice = Lattice(system='cubic',structure_type='face_centered', dimension='3D')

# Se crea la base de átomos
base = Base(lattice_vectors= lattice.vectors, atoms=[[atom1, [0,0,0]],[atom2, [0.5,0,0]],[atom2, [0,0.5,0]],[atom2, [0,0,0.5]]], dimension='3D')

#Se grafica la base de atomos en un punto de red
base.plot()
```
Como notamos en el ejemplo la clase Base se inicializa pasándole los vectores de la red, una lista que contiene listas de los átomos creados, con su vector posición en la base a formar y la dimensión en la que se describirá.

### Crear estructurá cristalina
Con los dos conceptos previamente mostrados podemos formar lo que se conoce como estructura cristalina o cristal, siendo esta estructura la unión de una red de Bravais con una base de átomos, para ello a continuación se muestra un ejemplo de como construirla:

```python
# Se importan los modulos Lattice, Atom, Base y CristalStruture.
%matplotlib widget
from PySolidState.crystal_structure.lattice import Lattice
from PySolidState.crystal_structure.atom import Atom
from PySolidState.crystal_structure.base import Base
from PySolidState.crystal_structure.crystalStructure import CrystalStructure

#Se crean los átomos que harán parte de la base de átomos.
atom2 = Atom(name='Na+', size= 0.2, color= 'orangered')
atom1 = Atom(name='Cl-', size= 0.3, color= 'springgreen')

#Se crea la red de Bravais en la cual se acomodara la base de atomos.
lattice = Lattice(system='cubic',structure_type='face_centered', dimension='3D')
# Se crea la base de átomos
base = Base(lattice_vectors= lattice.vectors, atoms=[[atom1, [0,0,0]],[atom2, [0.5,0,0]],[atom2, [0,0.5,0]],[atom2, [0,0,0.5]]], dimension='3D')

# Se crea la estructura cristalina o cristal uniendo la red y la base ya creadas
crs = CrystalStructure(lattice=lattice, base=base, dimension='3D')
#Se crea la figura de la red cristalina o cristal Na+Cl- (Cloruro de Sodio)
crs.plot()
```

