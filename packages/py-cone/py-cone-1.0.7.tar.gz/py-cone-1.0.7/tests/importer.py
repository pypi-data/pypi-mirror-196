import pathlib


def import_cls_from_path(path):
  
  if isinstance(path, str):
    path = pathlib.Path(path)
  path_or_file = path.glob("*")
  path
  for f in path_or_file:
    if f.is_file():
      if f.name == "__init__.py":
        continue
      module_name = f.name.split(".")[0]
      module = __import__(f"{path.name}.{module_name}", fromlist=[module_name])
      cls = getattr(module, module_name)
      return cls
    else:
      return import_cls_from_path(f)
  
  return None

if __name__ == "__main__":
  cls = import_cls_from_path("tests")
  print(cls)