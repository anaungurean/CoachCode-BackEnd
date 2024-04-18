import requests

if __name__ == '__main__':
    url = 'http://localhost:5000/test'  # Adresa serverului tău Flask

    data = {
        'language': 'python',
        'code': '''
class Solution(object):
    def twoSum(self, nums, target):
        for index_1 in range(0, len(nums)):
            for index_2 in range(index_1 + 1, len(nums)):
                if nums[index_1] + nums[index_2] == target:
                    return (index_1, index_2)

solution = Solution()
num_input = input().strip()
nums = list(map(int, num_input.split()))
target = int(input().strip())
print(solution.twoSum(nums, target))
''',
        'input': "2 7 11 15\n9",  # Datele de intrare în format JSON
        'expected_output': "[0, 1]"  # Rezultatul așteptat
    }

    response = requests.post(url, json=data)


    if response.status_code == 200:
        print(response.json())
    else:
        print("Request failed with status code:", response.status_code)

    data = {
        'language': 'java',
        'code': '''
 import java.util.*;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        for (int index_1 = 0; index_1 < nums.length; index_1++) {
            for (int index_2 = index_1 + 1; index_2 < nums.length; index_2++) {
                if (nums[index_1] + nums[index_2] == target) {
                    return new int[]{index_1, index_2};
                }
            }
        }
        return new int[0];
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Introduceti elementele listei nums separate prin spatiu:");
        String numInput = scanner.nextLine().trim();
        String[] numStrings = numInput.split(" ");
        int[] nums = new int[numStrings.length];
        for (int i = 0; i < numStrings.length; i++) {
            nums[i] = Integer.parseInt(numStrings[i]);
        }

        System.out.println("Introduceti valoarea target: ");
        int target = scanner.nextInt();

        Solution solution = new Solution();
        int[] result = solution.twoSum(nums, target);
        if (result.length == 2) {
            System.out.println("Indicii perechii care aduna " + target + " sunt: [" + result[0] + ", " + result[1] + "]");
        } else {
            System.out.println("Nu s-a gasit nicio pereche cu suma " + target);
        }
    }
}
''',
        'input': "2 7 11 15\n9",  # Datele de intrare în format JSON
        'expected_output': "[0, 1]"  # Rezultatul așteptat
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print(response.json())
    else:
        print("Request failed with status code:", response.status_code)
