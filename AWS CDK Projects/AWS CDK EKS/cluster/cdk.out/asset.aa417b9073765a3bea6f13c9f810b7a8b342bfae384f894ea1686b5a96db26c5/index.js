"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.isComplete = exports.onEvent = void 0;
// eslint-disable-next-line import/no-extraneous-dependencies
const aws = require("aws-sdk");
const cluster_1 = require("./cluster");
const consts = require("./consts");
const fargate_1 = require("./fargate");
aws.config.logger = console;
let eks;
const defaultEksClient = {
    createCluster: req => getEksClient().createCluster(req).promise(),
    deleteCluster: req => getEksClient().deleteCluster(req).promise(),
    describeCluster: req => getEksClient().describeCluster(req).promise(),
    describeUpdate: req => getEksClient().describeUpdate(req).promise(),
    updateClusterConfig: req => getEksClient().updateClusterConfig(req).promise(),
    updateClusterVersion: req => getEksClient().updateClusterVersion(req).promise(),
    createFargateProfile: req => getEksClient().createFargateProfile(req).promise(),
    deleteFargateProfile: req => getEksClient().deleteFargateProfile(req).promise(),
    describeFargateProfile: req => getEksClient().describeFargateProfile(req).promise(),
    configureAssumeRole: req => {
        console.log(JSON.stringify({ assumeRole: req }, undefined, 2));
        const creds = new aws.ChainableTemporaryCredentials({
            params: req,
        });
        eks = new aws.EKS({ credentials: creds });
    },
};
function getEksClient() {
    if (!eks) {
        throw new Error('EKS client not initialized (call "configureAssumeRole")');
    }
    return eks;
}
async function onEvent(event) {
    const provider = createResourceHandler(event);
    return provider.onEvent();
}
exports.onEvent = onEvent;
async function isComplete(event) {
    const provider = createResourceHandler(event);
    return provider.isComplete();
}
exports.isComplete = isComplete;
function createResourceHandler(event) {
    switch (event.ResourceType) {
        case consts.CLUSTER_RESOURCE_TYPE: return new cluster_1.ClusterResourceHandler(defaultEksClient, event);
        case consts.FARGATE_PROFILE_RESOURCE_TYPE: return new fargate_1.FargateProfileResourceHandler(defaultEksClient, event);
        default:
            throw new Error(`Unsupported resource type "${event.ResourceType}`);
    }
}
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyJpbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7QUFHQSw2REFBNkQ7QUFDN0QsK0JBQStCO0FBQy9CLHVDQUFtRDtBQUVuRCxtQ0FBbUM7QUFDbkMsdUNBQTBEO0FBRTFELEdBQUcsQ0FBQyxNQUFNLENBQUMsTUFBTSxHQUFHLE9BQU8sQ0FBQztBQUU1QixJQUFJLEdBQXdCLENBQUM7QUFFN0IsTUFBTSxnQkFBZ0IsR0FBYztJQUNsQyxhQUFhLEVBQUUsR0FBRyxDQUFDLEVBQUUsQ0FBQyxZQUFZLEVBQUUsQ0FBQyxhQUFhLENBQUMsR0FBRyxDQUFDLENBQUMsT0FBTyxFQUFFO0lBQ2pFLGFBQWEsRUFBRSxHQUFHLENBQUMsRUFBRSxDQUFDLFlBQVksRUFBRSxDQUFDLGFBQWEsQ0FBQyxHQUFHLENBQUMsQ0FBQyxPQUFPLEVBQUU7SUFDakUsZUFBZSxFQUFFLEdBQUcsQ0FBQyxFQUFFLENBQUMsWUFBWSxFQUFFLENBQUMsZUFBZSxDQUFDLEdBQUcsQ0FBQyxDQUFDLE9BQU8sRUFBRTtJQUNyRSxjQUFjLEVBQUUsR0FBRyxDQUFDLEVBQUUsQ0FBQyxZQUFZLEVBQUUsQ0FBQyxjQUFjLENBQUMsR0FBRyxDQUFDLENBQUMsT0FBTyxFQUFFO0lBQ25FLG1CQUFtQixFQUFFLEdBQUcsQ0FBQyxFQUFFLENBQUMsWUFBWSxFQUFFLENBQUMsbUJBQW1CLENBQUMsR0FBRyxDQUFDLENBQUMsT0FBTyxFQUFFO0lBQzdFLG9CQUFvQixFQUFFLEdBQUcsQ0FBQyxFQUFFLENBQUMsWUFBWSxFQUFFLENBQUMsb0JBQW9CLENBQUMsR0FBRyxDQUFDLENBQUMsT0FBTyxFQUFFO0lBQy9FLG9CQUFvQixFQUFFLEdBQUcsQ0FBQyxFQUFFLENBQUMsWUFBWSxFQUFFLENBQUMsb0JBQW9CLENBQUMsR0FBRyxDQUFDLENBQUMsT0FBTyxFQUFFO0lBQy9FLG9CQUFvQixFQUFFLEdBQUcsQ0FBQyxFQUFFLENBQUMsWUFBWSxFQUFFLENBQUMsb0JBQW9CLENBQUMsR0FBRyxDQUFDLENBQUMsT0FBTyxFQUFFO0lBQy9FLHNCQUFzQixFQUFFLEdBQUcsQ0FBQyxFQUFFLENBQUMsWUFBWSxFQUFFLENBQUMsc0JBQXNCLENBQUMsR0FBRyxDQUFDLENBQUMsT0FBTyxFQUFFO0lBQ25GLG1CQUFtQixFQUFFLEdBQUcsQ0FBQyxFQUFFO1FBQ3pCLE9BQU8sQ0FBQyxHQUFHLENBQUMsSUFBSSxDQUFDLFNBQVMsQ0FBQyxFQUFFLFVBQVUsRUFBRSxHQUFHLEVBQUUsRUFBRSxTQUFTLEVBQUUsQ0FBQyxDQUFDLENBQUMsQ0FBQztRQUMvRCxNQUFNLEtBQUssR0FBRyxJQUFJLEdBQUcsQ0FBQyw2QkFBNkIsQ0FBQztZQUNsRCxNQUFNLEVBQUUsR0FBRztTQUNaLENBQUMsQ0FBQztRQUVILEdBQUcsR0FBRyxJQUFJLEdBQUcsQ0FBQyxHQUFHLENBQUMsRUFBRSxXQUFXLEVBQUUsS0FBSyxFQUFFLENBQUMsQ0FBQztJQUM1QyxDQUFDO0NBQ0YsQ0FBQztBQUVGLFNBQVMsWUFBWTtJQUNuQixJQUFJLENBQUMsR0FBRyxFQUFFO1FBQ1IsTUFBTSxJQUFJLEtBQUssQ0FBQyx5REFBeUQsQ0FBQyxDQUFDO0tBQzVFO0lBRUQsT0FBTyxHQUFHLENBQUM7QUFDYixDQUFDO0FBRU0sS0FBSyxVQUFVLE9BQU8sQ0FBQyxLQUFrRDtJQUM5RSxNQUFNLFFBQVEsR0FBRyxxQkFBcUIsQ0FBQyxLQUFLLENBQUMsQ0FBQztJQUM5QyxPQUFPLFFBQVEsQ0FBQyxPQUFPLEVBQUUsQ0FBQztBQUM1QixDQUFDO0FBSEQsMEJBR0M7QUFFTSxLQUFLLFVBQVUsVUFBVSxDQUFDLEtBQWtEO0lBQ2pGLE1BQU0sUUFBUSxHQUFHLHFCQUFxQixDQUFDLEtBQUssQ0FBQyxDQUFDO0lBQzlDLE9BQU8sUUFBUSxDQUFDLFVBQVUsRUFBRSxDQUFDO0FBQy9CLENBQUM7QUFIRCxnQ0FHQztBQUVELFNBQVMscUJBQXFCLENBQUMsS0FBa0Q7SUFDL0UsUUFBUSxLQUFLLENBQUMsWUFBWSxFQUFFO1FBQzFCLEtBQUssTUFBTSxDQUFDLHFCQUFxQixDQUFDLENBQUMsT0FBTyxJQUFJLGdDQUFzQixDQUFDLGdCQUFnQixFQUFFLEtBQUssQ0FBQyxDQUFDO1FBQzlGLEtBQUssTUFBTSxDQUFDLDZCQUE2QixDQUFDLENBQUMsT0FBTyxJQUFJLHVDQUE2QixDQUFDLGdCQUFnQixFQUFFLEtBQUssQ0FBQyxDQUFDO1FBQzdHO1lBQ0UsTUFBTSxJQUFJLEtBQUssQ0FBQyw4QkFBOEIsS0FBSyxDQUFDLFlBQVksRUFBRSxDQUFDLENBQUM7S0FDdkU7QUFDSCxDQUFDIiwic291cmNlc0NvbnRlbnQiOlsiLyogZXNsaW50LWRpc2FibGUgbm8tY29uc29sZSAqL1xuLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIGltcG9ydC9uby1leHRyYW5lb3VzLWRlcGVuZGVuY2llc1xuaW1wb3J0IHsgSXNDb21wbGV0ZVJlc3BvbnNlIH0gZnJvbSAnQGF3cy1jZGsvY3VzdG9tLXJlc291cmNlcy9saWIvcHJvdmlkZXItZnJhbWV3b3JrL3R5cGVzJztcbi8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBpbXBvcnQvbm8tZXh0cmFuZW91cy1kZXBlbmRlbmNpZXNcbmltcG9ydCAqIGFzIGF3cyBmcm9tICdhd3Mtc2RrJztcbmltcG9ydCB7IENsdXN0ZXJSZXNvdXJjZUhhbmRsZXIgfSBmcm9tICcuL2NsdXN0ZXInO1xuaW1wb3J0IHsgRWtzQ2xpZW50IH0gZnJvbSAnLi9jb21tb24nO1xuaW1wb3J0ICogYXMgY29uc3RzIGZyb20gJy4vY29uc3RzJztcbmltcG9ydCB7IEZhcmdhdGVQcm9maWxlUmVzb3VyY2VIYW5kbGVyIH0gZnJvbSAnLi9mYXJnYXRlJztcblxuYXdzLmNvbmZpZy5sb2dnZXIgPSBjb25zb2xlO1xuXG5sZXQgZWtzOiBhd3MuRUtTIHwgdW5kZWZpbmVkO1xuXG5jb25zdCBkZWZhdWx0RWtzQ2xpZW50OiBFa3NDbGllbnQgPSB7XG4gIGNyZWF0ZUNsdXN0ZXI6IHJlcSA9PiBnZXRFa3NDbGllbnQoKS5jcmVhdGVDbHVzdGVyKHJlcSkucHJvbWlzZSgpLFxuICBkZWxldGVDbHVzdGVyOiByZXEgPT4gZ2V0RWtzQ2xpZW50KCkuZGVsZXRlQ2x1c3RlcihyZXEpLnByb21pc2UoKSxcbiAgZGVzY3JpYmVDbHVzdGVyOiByZXEgPT4gZ2V0RWtzQ2xpZW50KCkuZGVzY3JpYmVDbHVzdGVyKHJlcSkucHJvbWlzZSgpLFxuICBkZXNjcmliZVVwZGF0ZTogcmVxID0+IGdldEVrc0NsaWVudCgpLmRlc2NyaWJlVXBkYXRlKHJlcSkucHJvbWlzZSgpLFxuICB1cGRhdGVDbHVzdGVyQ29uZmlnOiByZXEgPT4gZ2V0RWtzQ2xpZW50KCkudXBkYXRlQ2x1c3RlckNvbmZpZyhyZXEpLnByb21pc2UoKSxcbiAgdXBkYXRlQ2x1c3RlclZlcnNpb246IHJlcSA9PiBnZXRFa3NDbGllbnQoKS51cGRhdGVDbHVzdGVyVmVyc2lvbihyZXEpLnByb21pc2UoKSxcbiAgY3JlYXRlRmFyZ2F0ZVByb2ZpbGU6IHJlcSA9PiBnZXRFa3NDbGllbnQoKS5jcmVhdGVGYXJnYXRlUHJvZmlsZShyZXEpLnByb21pc2UoKSxcbiAgZGVsZXRlRmFyZ2F0ZVByb2ZpbGU6IHJlcSA9PiBnZXRFa3NDbGllbnQoKS5kZWxldGVGYXJnYXRlUHJvZmlsZShyZXEpLnByb21pc2UoKSxcbiAgZGVzY3JpYmVGYXJnYXRlUHJvZmlsZTogcmVxID0+IGdldEVrc0NsaWVudCgpLmRlc2NyaWJlRmFyZ2F0ZVByb2ZpbGUocmVxKS5wcm9taXNlKCksXG4gIGNvbmZpZ3VyZUFzc3VtZVJvbGU6IHJlcSA9PiB7XG4gICAgY29uc29sZS5sb2coSlNPTi5zdHJpbmdpZnkoeyBhc3N1bWVSb2xlOiByZXEgfSwgdW5kZWZpbmVkLCAyKSk7XG4gICAgY29uc3QgY3JlZHMgPSBuZXcgYXdzLkNoYWluYWJsZVRlbXBvcmFyeUNyZWRlbnRpYWxzKHtcbiAgICAgIHBhcmFtczogcmVxLFxuICAgIH0pO1xuXG4gICAgZWtzID0gbmV3IGF3cy5FS1MoeyBjcmVkZW50aWFsczogY3JlZHMgfSk7XG4gIH0sXG59O1xuXG5mdW5jdGlvbiBnZXRFa3NDbGllbnQoKSB7XG4gIGlmICghZWtzKSB7XG4gICAgdGhyb3cgbmV3IEVycm9yKCdFS1MgY2xpZW50IG5vdCBpbml0aWFsaXplZCAoY2FsbCBcImNvbmZpZ3VyZUFzc3VtZVJvbGVcIiknKTtcbiAgfVxuXG4gIHJldHVybiBla3M7XG59XG5cbmV4cG9ydCBhc3luYyBmdW5jdGlvbiBvbkV2ZW50KGV2ZW50OiBBV1NMYW1iZGEuQ2xvdWRGb3JtYXRpb25DdXN0b21SZXNvdXJjZUV2ZW50KSB7XG4gIGNvbnN0IHByb3ZpZGVyID0gY3JlYXRlUmVzb3VyY2VIYW5kbGVyKGV2ZW50KTtcbiAgcmV0dXJuIHByb3ZpZGVyLm9uRXZlbnQoKTtcbn1cblxuZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIGlzQ29tcGxldGUoZXZlbnQ6IEFXU0xhbWJkYS5DbG91ZEZvcm1hdGlvbkN1c3RvbVJlc291cmNlRXZlbnQpOiBQcm9taXNlPElzQ29tcGxldGVSZXNwb25zZT4ge1xuICBjb25zdCBwcm92aWRlciA9IGNyZWF0ZVJlc291cmNlSGFuZGxlcihldmVudCk7XG4gIHJldHVybiBwcm92aWRlci5pc0NvbXBsZXRlKCk7XG59XG5cbmZ1bmN0aW9uIGNyZWF0ZVJlc291cmNlSGFuZGxlcihldmVudDogQVdTTGFtYmRhLkNsb3VkRm9ybWF0aW9uQ3VzdG9tUmVzb3VyY2VFdmVudCkge1xuICBzd2l0Y2ggKGV2ZW50LlJlc291cmNlVHlwZSkge1xuICAgIGNhc2UgY29uc3RzLkNMVVNURVJfUkVTT1VSQ0VfVFlQRTogcmV0dXJuIG5ldyBDbHVzdGVyUmVzb3VyY2VIYW5kbGVyKGRlZmF1bHRFa3NDbGllbnQsIGV2ZW50KTtcbiAgICBjYXNlIGNvbnN0cy5GQVJHQVRFX1BST0ZJTEVfUkVTT1VSQ0VfVFlQRTogcmV0dXJuIG5ldyBGYXJnYXRlUHJvZmlsZVJlc291cmNlSGFuZGxlcihkZWZhdWx0RWtzQ2xpZW50LCBldmVudCk7XG4gICAgZGVmYXVsdDpcbiAgICAgIHRocm93IG5ldyBFcnJvcihgVW5zdXBwb3J0ZWQgcmVzb3VyY2UgdHlwZSBcIiR7ZXZlbnQuUmVzb3VyY2VUeXBlfWApO1xuICB9XG59XG4iXX0=