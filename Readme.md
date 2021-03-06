# Artifactorium

Path manager which stores and builds paths for experiment tracking.

Built on top of the *pathlib* standard library for your convenience.
  
## Installation

Artifactorium can be installed by issuing the following command:

`pip install https://github.com/csxeba/Artifactorium.git`

## Usage


### Instantiation

The library presents an OOP API and is intended to be simply imported by issuing

```python
from artifactorium import Artifactorium

artifactorium = Artifactorium("/data/experiments", "ml", "NOW")
```

An **Artifactorium** instance is associated with one specific experimental setup.
A series of experiments should be tracked by separate **Artifactorium** instances.

**Artifactorium** supports arbitrary nested root paths, so the user groups his or
her directories however they want.

The special string 'NOW' will be replaced by the current date and time.


### Registering paths

After an instance has been created, subdirectories can be registered, for
storing and separating different artifacts of an experiment.

```python
artifactorium.register_path(property_name="tensorboard", path="logs/tensorboard")
artifactorium.register_path("tensorboard", "logs", "NOW", "tensorboard")
```

These will register the supplied directory under the artifactorium root with the
'tensorboard' property name.
 
In the simple case, when the desired path is simply artifactory_root/property_name,
one can use the simple form:

```python
artifactorium.register_path("tensorboard")
```

Which registers "artifactory_root/tensorboard" under the property name "tensorboard".

File paths are a bit tricky because of the lazy evaluation. They can be registered
by explicitly telling Artifactorium that the path is to be handles as a file,
unless the lazy evaluation will create our file as a directory and makes our
lives difficult.

So please indicate when registering a file:

```python
artifactorium.register_path("csv_log", "logs/runlog.csv", is_file=True)
```

#### Note on code completion

This type of dynamic property creation does not go well with modern IDEs.
There is one thing we can do to at least get code completion. An example will
be shown for this in the *Examples* section.

### Resetting paths

The root directory will always be registered under the "root" property, which cannot
be reset. Any other **properties can be freely set and reset by default**. If this
is not the desired behaviour, the `allow_reset_properties` constructor parameter
can be set to `False`, in which case a PropertyAlreadySetError will be thrown,
which is defined in *artifactory.exception*.


### Accessing registered paths

Registered paths can be accessed the following ways:

```python
artifactorium.tensorboard
artifactorium["tensorboard"]
```

The paths returned by the instance are pathlib.Path objects by default. Please note
that some libraries do not fully support passing Path objects to them, in which
case you either need to manually cast the Path objects to strings or set the
constructor parameter `return_paths_as_strings` to `True`.

### Note on laziness

The directories (including the the artifactorium root) will only be created, if they
are accessed by the user after creation. Please note that because of this, when you
register a file path, you must indicate that it is a path to a file, or a directory
will be created under your file name when you try to access your registered file
path.

## Example

Say I am into *Deep Reinforcement Learning* and *Data Science* and I am working on two sets of experiments:
  - One RL experiment for a blog post, where I am aiming to generate *TensorBoard*
    event files, CSV training logs and videos of my model trying to play the
    *Atari* game *Pong* against the built-in AI.
  - One data exporation experiment, where I generate nice plots from a big dataset.

I store all my files under */data/experiments*, but I would like to separate the RL
stuff from the data exporation stuff. For a single RL experiment, I could create an
**Artifactorium** instance like this:

```python
import tensorflow as tf

from artifactorium import Artifactorium

artifactory = Artifactorium("/data/experiments", "reinforcement", "PPO", "Pong-v0", "NOW")
artifactory.register_path("tensorboard", "logs/tensorboard")
artifactory.register_path("csv_logs", "logs/csv/runlog.csv")
artifactory.register_path("renders")
artifactory.register_path("model_checkpoints")

...  # Secret Reinforcement Learning magic is happening here

ppo_actor_critic_model = ...  # we generate some artifact

# The pathlib syntax is used to append the 
# filename to the checkpoints directory path.
save_path = artifactory.checkpoints / "checkpoint_epoch_100.h5"

# The pathlib Path is converted back to a unicode string
# by casting it to str() to ensure compatibility.
ppo_actor_critic_model.save(str(save_path))
```

Afterwards, when I'm working on my data exploration project, I use the library
like so:

```python
from sklearn import decomposition
from matplotlib import pyplot as plt

from artifactorium import Artifactorium

artifactory = Artifactorium("/data/experiments", "data_science", "iris", "NOW")
artifactory.register_path("plots")
artifactory.register_path("config", "experiment_config.json", is_file=True)

...  # Secret Data Science magic is happening here

pca_data = ...
lda_data = ...

plt.figure()
plt.scatter(pca_data[:, 0], pca_data[:, 1], "rx")
plt.grid()
plt.savefig(artifactory.plots / "pca_transform.png") 
plt.clf()

plt.figure()
plt.scatter(lda_data[:, 0], lda_data[:, 1], "rx")
plt.grid()
plt.savefig(artifactory.plots / "lda_transform.png")
```

Below is an example on how to use Artifactorium and get code completion for
modern IDEs.

The secret is to derive a class from Artifactorium and define the \_\_slots\_\_
attribute for our subclass. 

```python
from artifactorium import Artifactorium


class MyArtifactorium(Artifactorium):

    __slots__ = "logs", "checkpoints"

    def __init__(self):
        super().__init__(self, "root")
        self.register_path("logs")
        self.register_path("checkpoints")
```

This way, the IDE will get a hint for what property names will be available.
However, using slots restricts some functionalities of Python classes. You can
educate yourself about slots in the Python docs:
[3. Data model](https://docs.python.org/3/reference/datamodel.html#slots)

## Thanks

Thank you for using Artifactorium! Any bugs, improvement suggestions can be
filed as an issue on the GitHub!

Pull requests are also welcome!
