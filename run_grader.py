from generator import demonstrate_shannon_concepts, InformationAnalyzer, MarkovTextGenerator, CreativeTextGenerator
from assignment3_grading_tester import Assignment3GradingTester

student_classes = {
    'demonstrate_shannon_concepts': demonstrate_shannon_concepts,
    'InformationAnalyzer': InformationAnalyzer,
    'MarkovTextGenerator': MarkovTextGenerator,
    'CreativeTextGenerator': CreativeTextGenerator
}

tester = Assignment3GradingTester()
tester.test_comprehensive_functionality(student_classes)
