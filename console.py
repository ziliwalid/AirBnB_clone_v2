#!/usr/bin/python3
"""Defines the HBNB console."""
import cmd
from shlex import split
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }

    def emptyline(self):
        """Ignore empty lines."""
        pass

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """Create a new class instance with given keys/values and print its id."""
        try:
            if not line:
                raise SyntaxError()
            input_list = line.split(" ")

            kwargs = {}
            for i in range(1, len(input_list)):
                key, value = tuple(input_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(input_list[0])()
            else:
                obj = eval(input_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Prints the string representation of an instance."""
        try:
            if not line:
                raise SyntaxError()
            input_list = line.split(" ")
            if input_list[0] not in self.__classes:
                raise NameError()
            if len(input_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = input_list[0] + '.' + input_list[1]
            if key in objects:
                print(objects[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id."""
        try:
            if not line:
                raise SyntaxError()
            input_list = line.split(" ")
            if input_list[0] not in self.__classes:
                raise NameError()
            if len(input_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = input_list[0] + '.' + input_list[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, line):
        """Display string representations of all instances of a given class."""
        if not line:
            o = storage.all()
            print([o[k].__str__() for k in o])
            return
        try:
            args = line.split(" ")
            if args[0] not in self.__classes:
                raise NameError()

            o = storage.all(eval(args[0]))
            print([o[k].__str__() for k in o])

        except NameError:
            print("** class doesn't exist **")

    def do_update(self, line):
        """Updates an instance by adding or updating attribute."""
        try:
            if not line:
                raise SyntaxError()
            input_list = split(line, " ")
            if input_list[0] not in self.__classes:
                raise NameError()
            if len(input_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = input_list[0] + '.' + input_list[1]
            if key not in objects:
                raise KeyError()
            if len(input_list) < 3:
                raise AttributeError()
            if len(input_list) < 4:
                raise ValueError()
            v = objects[key]
            try:
                v.__dict__[input_list[2]] = eval(input_list[3])
            except Exception:
                v.__dict__[input_list[2]] = input_list[3]
                v.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def count(self, line):
        """Count the number of instances of a class."""
        counter = 0
        try:
            input_list = split(line, " ")
            if input_list[0] not in self.__classes:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == input_list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """Strip the argument and return a string of command."""
        new_list = []
        new_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, line):
        """Retrieve all instances of a class and retrieve the number of instances."""
        input_list = line.split('.')
        if len(input_list) >= 2:
            if input_list[1] == "all()":
                self.do_all(input_list[0])
            elif input_list[1] == "count()":
                self.count(input_list[0])
            elif input_list[1][:4] == "show":
                self.do_show(self.strip_clean(input_list))
            elif input_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(input_list))
            elif input_list[1][:6] == "update":
                args = self.strip_clean(input_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()

