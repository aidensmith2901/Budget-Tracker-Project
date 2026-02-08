#include <iostream>
#include <string>
 
int menu() {
    std::string menuChoice;
    int num = 0;  // Declare once, outside the blocks

    std::cout << "Welcome to the number guessing game!\n\n"
              << "Select a difficulty\n"
              << "1. Easy\n"
              << "2. Medium\n"
              << "3. Hard\n"
              << "4. Impossible\n\n";

    std::cout << "SELECTION: ";
    std::getline(std::cin, menuChoice);

    if (!menuChoice.empty()) {
        num = std::stoi(menuChoice);  // Assign value if not empty
    }

    return num;
}

int gameSetup(int choice){
    int min = 0;
    int ans = 0;
    int max = 0;
    std::srand(std::time(0));
    if (choice == 1) {
        int max = 2;
        int resp;
        int ans = std::rand() % (max - min);}
    if (choice == 2) {
        int max = 10;
        int resp;
        int ans = std::rand() % (max - min);}
    if (choice == 3) {
        int max = 100;
        int resp;
        int ans = std::rand() % (max - min);}
    if (choice == 4) {
        int max = 1000;
        int resp;
        int ans = std::rand() % (max - min);}

    int resp;
    std::cout << "Enter a number between " << min << " and " << max << ": ";
    std::cin >> resp;
    std::cout << "\n";
    if (resp == ans) {std::cout << "That is correct, you win!";} 
    else {std::cout << "That is wrong. The correct answer is " << ans;}
    
    return 0;


}
/*
void gameRun(int min, int max, int ans){

    int resp;
    std::cout << "Enter a number between " << min << " and " << max << ": ";
    std::cin >> resp;
    std::cout << "\n";
    if (resp == ans) {std::cout << "That is correct, you win!";} 
    else {std::cout << "That is wrong. The correct answer is " << ans;}

}
*/
int main() {

    int choice = menu();
    if (choice != 0){
        system("CLS");
        gameSetup(choice);

        //gameRun(min, max, ans);

    }
    
    else {

        system("CLS");
        std::cout << "Nothing selected\nExiting gane...";
    }

    return 0;
}
