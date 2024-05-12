'''
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
'''

'''
import java.util.Scanner;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        int n = nums.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                if (nums[i] + nums[j] == target) {
                    return new int[]{i, j};
                }
            }
        }
        return new int[]{}; 

    }
}

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Solution solution = new Solution();

        String[] numInput = scanner.nextLine().split(" ");
        int[] nums = new int[numInput.length];
        for (int i = 0; i < numInput.length; i++) {
            nums[i] = Integer.parseInt(numInput[i]);
        }

        int target = scanner.nextInt();

        int[] result = solution.twoSum(nums, target);
        if (result.length == 2) {
            System.out.println(result[0] + " " + result[1]);
        } else {
            System.out.println(" ");
        }
    } 
}
'''



