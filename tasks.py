# Declare the sub-module collections
from invoke import Collection

from mantium_client.invoke_tasks import build, test

namespace = Collection()
namespace.add_collection(Collection.from_module(build))
namespace.add_collection(Collection.from_module(test))
