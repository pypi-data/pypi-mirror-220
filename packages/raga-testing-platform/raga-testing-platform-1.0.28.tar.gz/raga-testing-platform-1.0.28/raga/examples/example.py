from raga import *
import pandas as pd

pd_data_frame = pd.read_pickle('TestingDataFrame.pkl')

#create schema object of RagaSchema instance
schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement(), pd_data_frame)
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame)
schema.add("SourceLink", FeatureSchemaElement(), pd_data_frame)
schema.add("Reflection", AttributeSchemaElement(), pd_data_frame)
schema.add("Overlap", AttributeSchemaElement(), pd_data_frame)
schema.add("CameraAngle", AttributeSchemaElement(), pd_data_frame)
schema.add("AnnotationsV1", InferenceSchemaElement(model="Testing-modelA"), pd_data_frame)
schema.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="Testing-modelA", ref_col_name=""), pd_data_frame)
schema.add("ROIVectorsM1", RoiEmbeddingSchemaElement(model="Testing-modelA", ref_col_name=""), pd_data_frame)
schema.add("AnnotationsV2", InferenceSchemaElement(model="Testing-modelB"), pd_data_frame)
schema.add("ImageVectorsM2", ImageEmbeddingSchemaElement(model="Testing-modelB", ref_col_name=""), pd_data_frame)
schema.add("ROIVectorsM2", RoiEmbeddingSchemaElement(model="Testing-modelB", ref_col_name=""), pd_data_frame)

#create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject",run_name= "test-exp-jun-new-4")

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, name="test-dataset-jun-new-1")

#load schema and pandas data frame
test_ds.load(pd_data_frame, schema)


#Params for unlabelled AB Model Testing
# testName = StringElement("test-unlabelled-1")
# modelA = StringElement("Testing-modelA")
# modelB = StringElement("Testing-modelB")
# type = ModelABTestTypeElement("labelled")
# aggregation_level = AggregationLevelElement()
# aggregation_level.add(StringElement("Reflection"))
# aggregation_level.add(StringElement("Overlap"))
# aggregation_level.add(StringElement("CameraAngle"))
# rules = ModelABTestRules()
# rules.add(metric = StringElement("difference_percentage"), IoU = FloatElement(0.5), _class = StringElement("ALL"), threshold = FloatElement(0.2))
# rules.add(metric = StringElement("difference_count"), IoU = FloatElement(0.5), _class = StringElement("canned_food"), threshold = FloatElement(0.5))

# #create payload for model ab testing
# model_comparison_check = model_ab_test(test_ds, testName=testName, modelA = modelA , modelB = modelB , type = type, aggregation_level = aggregation_level, rules = rules)

# #add payload into test_session object
# test_session.add(model_comparison_check)

# #run added ab test model payload
# test_session.run()