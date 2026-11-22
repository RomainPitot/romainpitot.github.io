// Prototype: a MOBA-style turret. Creeps are targeted before the player,
// and a locked target is never swapped while it stays in range.
public class TurretScript : MonoBehaviour
{
    public Transform turretHead;
    public float rotationSpeed = 5f;
    public float fireRate = 1f;        // shots per second

    private Transform target;

    void OnTriggerEnter(Collider other)
    {
        // Already locked on: keep the target.
        if (target != null) return;

        // Creeps first...
        if (other.CompareTag("Creeps"))
        {
            target = other.transform;
            return;
        }

        // ...and the player only if nothing else is in range.
        if (other.CompareTag("Player"))
            target = other.transform;
    }

    void OnTriggerExit(Collider other)
    {
        if (other.transform == target)
            target = null;             // target left the zone: free the turret
    }

    void AimAtTarget()
    {
        Vector3 direction = target.position - turretHead.position;
        Quaternion lookRot = Quaternion.LookRotation(direction);
        turretHead.rotation = Quaternion.Slerp(
            turretHead.rotation, lookRot, rotationSpeed * Time.deltaTime);
    }
}
