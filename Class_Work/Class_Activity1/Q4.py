# Area and Volume Calculator

print("Choose a shape:")
print("1. Circle")
print("2. Sphere")
print("3. Cone")
print("4. Pyramid")
print("5. Cylinder")
print("6. Rectangle")
print("7. Regular Polygon")

choice = int(input("Enter your choice: "))

if choice == 1:
    r = float(input("Enter radius: "))
    area = 3.14 * r * r
    print("Area of circle is:", area)
elif choice == 2:
    r = float(input("Enter radius: "))
    volume = (4 / 3) * 3.14 * r * r * r
    print("Volume of sphere is:", volume)
elif choice == 3:
    r = float(input("Enter radius: "))
    h = float(input("Enter height: "))
    volume = (1 / 3) * 3.14 * r * r * h
    print("Volume of cone is:", volume)
elif choice == 4:
    l = float(input("Enter length: "))
    w = float(input("Enter width: "))
    h = float(input("Enter height: "))
    volume = (1 / 3) * l * w * h
    print("Volume of pyramid is:", volume)
elif choice == 5:
    r = float(input("Enter radius: "))
    h = float(input("Enter height: "))
    volume = 3.14 * r * r * h
    print("Volume of cylinder is:", volume)
elif choice == 6:
    l = float(input("Enter length: "))
    w = float(input("Enter width: "))
    area = l * w
    print("Area of rectangle is:", area)
elif choice == 7:
    n = int(input("Enter number of sides: "))
    s = float(input("Enter side length: "))
    area = (n * s * s) / (4 * 3.14)
    print("Area of regular polygon is:", area)
else:
    print("Invalid choice")
