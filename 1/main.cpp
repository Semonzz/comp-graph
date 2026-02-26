#include <iostream>
#include <cmath>
#include <iomanip>

#define LD long double
#define PI acos(-1.0)

const LD EPS = 1e-9;

using namespace std;

// https://www.desmos.com/


struct Point2D {
    LD x, y;
};

struct Point3D {
    LD x, y, z;
};

void task1() {
    cout << "\n--- Задание 1 ---" << '\n';
    LD A, B, C;
    cout << "Введите коэффициенты прямой (A B C): ";
    cin >> A >> B >> C;

    Point2D p1, p2;
    cout << "Введите координаты точки 1 (x y): ";
    cin >> p1.x >> p1.y;
    cout << "Введите координаты точки 2 (x y): ";
    cin >> p2.x >> p2.y;

    LD f1 = A * p1.x + B * p1.y + C;
    LD f2 = A * p2.x + B * p2.y + C;

    cout << "Результат: ";
    if (fabsl(f1) < EPS && fabsl(f2) < EPS) {
        cout << "Обе точки лежат на прямой." << '\n';
    }
    else if (fabsl(f1) < EPS) {
        cout << "Точка 1 лежит на прямой, Точка 2 вне прямой." << '\n';
    }
    else if (fabsl(f2) < EPS) {
        cout << "Точка 2 лежит на прямой, Точка 1 вне прямой." << '\n';
    }
    else if ((f1 > 0 && f2 > 0) || (f1 < 0 && f2 < 0)) {
        cout << "Точки лежат по одну сторону от прямой." << '\n';
    }
    else {
        cout << "Точки лежат по разные стороны от прямой." << '\n';
    }
}

LD dotProduct2D(Point2D a, Point2D b) {
    return a.x * b.x + a.y * b.y;
}

bool isPointOnRay(Point2D P, Point2D Start, Point2D DirPoint) {
    Point2D vecRay = { DirPoint.x - Start.x, DirPoint.y - Start.y };
    Point2D vecP = { P.x - Start.x, P.y - Start.y };

    return dotProduct2D(vecRay, vecP) >= 0;
}

bool isCorrectRay(Point2D A, Point2D B) {
    if (fabsl(A.x - B.x) < EPS && fabsl(A.y - B.y) < EPS) return false;
    else return true;
}

bool areCollinear(Point2D A, Point2D B, Point2D C) {
    Point2D AB = { B.x - A.x, B.y - A.y };
    Point2D AC = { C.x - A.x, C.y - A.y };
    LD cross = AB.x * AC.y - AB.y * AC.x;
    return fabsl(cross) < EPS;
}

void task2() {
    cout << "\n--- Задание 2 ---" << '\n';
    Point2D A, B, C, D;
    cout << "Введите координаты точки A (x y): "; cin >> A.x >> A.y;
    cout << "Введите координаты точки B (x y): "; cin >> B.x >> B.y;
    cout << "Введите координаты точки C (x y): "; cin >> C.x >> C.y;
    cout << "Введите координаты точки D (x y): "; cin >> D.x >> D.y;

    if (!isCorrectRay(A, B)) {
        cout << "Ошибка: точки A и B совпадают! Луч [AB) не определён." << '\n';
        return;
    }
    if (!isCorrectRay(C, D)) {
        cout << "Ошибка: точки C и D совпадают! Луч [CD) не определён." << '\n';
        return;
    }
    if (!areCollinear(A, B, C) || !areCollinear(A, B, D)) {
        cout << "Ошибка: точки не лежат на одной прямой!" << '\n';
        return;
    }

    bool cOnAB = isPointOnRay(C, A, B);
    bool aOnCD = isPointOnRay(A, C, D);

    cout << "Результат: ";
    if (cOnAB || aOnCD) {
        cout << "Лучи [AB) и [CD) пересекаются." << '\n';
    }
    else {
        cout << "Лучи [AB) и [CD) не пересекаются." << '\n';
    }
}

LD getAngle(Point2D v) {
    LD angle = atan2l(v.y, v.x);
    if (angle < 0) angle += 2 * PI;
    return angle;
}

void task3() {
    cout << "\n--- Задание 3 ---" << '\n';
    Point2D A, B, C, D;
    cout << "Введите координаты точки A (x y): "; cin >> A.x >> A.y;
    cout << "Введите координаты точки B (вершина угла) (x y): "; cin >> B.x >> B.y;
    cout << "Введите координаты точки C (x y): "; cin >> C.x >> C.y;
    cout << "Введите координаты точки D (x y): "; cin >> D.x >> D.y;

    if (!isCorrectRay(B, A)) {
        cout << "Ошибка: точки A и B совпадают! Луч [BA) не определён." << '\n';
        return;
    }
    if (!isCorrectRay(B, C)) {
        cout << "Ошибка: точки C и B совпадают! Луч [BC) не определён." << '\n';
        return;
    }
    if (!isCorrectRay(B, D)) {
        cout << "Ошибка: точки B и D совпадают! Луч [BD) не определён." << '\n';
        return;
    }

    Point2D vecBA = { A.x - B.x, A.y - B.y };
    Point2D vecBC = { C.x - B.x, C.y - B.y };
    Point2D vecBD = { D.x - B.x, D.y - B.y };

    LD angleBA = getAngle(vecBA); //start
    LD angleBC = getAngle(vecBC); //end
    LD angleBD = getAngle(vecBD); //point

    bool inside = false;

    if (angleBA < angleBC) {
        if (angleBD > angleBA && angleBD < angleBC) inside = true;
    }
    else {
        if (angleBD > angleBA || angleBD < angleBC) inside = true;
    }

    cout << "Результат: ";
    if (inside) {
        cout << "Точка D лежит внутри угла ABC." << '\n';
    }
    else {
        cout << "Точка D НЕ лежит внутри угла ABC." << '\n';
    }
}

void task4() {
    cout << "\n--- Задание 4 ---" << '\n';
    LD A, B, C, D;
    cout << "Введите коэффициенты плоскости (A B C D): ";
    cin >> A >> B >> C >> D;

    Point3D p1, p2;
    cout << "Введите координаты точки 1 (x y z): ";
    cin >> p1.x >> p1.y >> p1.z;
    cout << "Введите координаты точки 2 (x y z): ";
    cin >> p2.x >> p2.y >> p2.z;

    LD f1 = A * p1.x + B * p1.y + C * p1.z + D;
    LD f2 = A * p2.x + B * p2.y + C * p2.z + D;

    cout << "Результат: ";
    if (fabsl(f1) < EPS && fabsl(f2) < EPS) {
        cout << "Обе точки лежат на плоскости." << '\n';
    }
    else if (fabsl(f1) < EPS) {
        cout << "Точка 1 лежит на плоскости, Точка 2 вне плоскости." << '\n';
    }
    else if (fabsl(f2) < EPS) {
        cout << "Точка 2 лежит на плоскости, Точка 1 вне плоскости." << '\n';
    }
    else if ((f1 > 0 && f2 > 0) || (f1 < 0 && f2 < 0)) {
        cout << "Точки лежат по одну сторону от плоскости." << '\n';
    }
    else {
        cout << "Точки лежат по разные стороны от плоскости." << '\n';
    }
}

void menu() {
    int choice;
    while (true) {
        cout << "\nВыберите задание для выполнения (1-4) или 0 для выхода: ";
        cin >> choice;

        switch (choice) {
        case 1: task1(); break;
        case 2: task2(); break;
        case 3: task3(); break;
        case 4: task4(); break;
        case 0: return;
        default: cout << "Неверный выбор." << '\n';
        }
    }
}

int main() {
    setlocale(LC_ALL, "Russian");
    cout << "Лабораторная работа №1. Аналитическая геометрия." << '\n';
    cout << "Решение для Варианта 6 всех заданий." << '\n';
    menu();
    return 0;
}
