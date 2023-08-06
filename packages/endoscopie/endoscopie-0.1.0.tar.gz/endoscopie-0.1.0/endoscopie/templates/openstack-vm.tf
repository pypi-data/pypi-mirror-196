terraform {
  required_providers {
    openstack = {
      source = "terraform-provider-openstack/openstack"
      version = "1.47.0"
    }
  }
}

provider "openstack" {
  # Identity v3 only
  application_credential_id     = "1aa3f014b91e4dde9b29f0ec98416581"
  application_credential_secret = "9m9XEXeZlyiIcqS8CfeUW0ferktgtofFZS77-rPxV1vojS1_m9JPDOr0B0efLKQLRgBscYDsIPEL4WJkHOaurQ"
  #user_domain_id                = "00865141787245159d1d12a6be9aeef3"
  #user_domain_name              = "kakaoicloudstage-r"
  #tenant_id                     = "eb014bc1f4d14b41a36823e2091c3a6d"
  #tenant_name                   = "set-manual-test"
  auth_url                      = "https://iam.sandbox.kakaoi.io/identity/v3"
  region                        = "kr-central-1"
}

    
    
resource "openstack_compute_instance_v2" "ubuntu-d1ad2360-5279-4e61-8609-8abe27f9b003-1" {
  name            = "ubuntu-d1ad2360-5279-4e61-8609-8abe27f9b003-1"
  flavor_id       = "3830ebad-ea2f-4822-8a7d-9e301c86a58d"
  key_pair        = "andy-cluster-keypair"
  user_data       = "${file("~/stage-andrew.sh")}"
  image_name      = "Ubuntu 18.04"
  security_groups = ["f4bc78e0-f25a-4fc1-9808-d0b7125d2155"]

  block_device {
    uuid                  = "d1ad2360-5279-4e61-8609-8abe27f9b003"
    source_type           = "image"
    volume_size           = 100
    boot_index            = 0
    destination_type      = "volume"
    delete_on_termination = true
  }

  network {
    uuid  = "0b8fb984-2726-432e-aa37-04b778ef2ba1"
  }
}
    

    
    
resource "openstack_compute_instance_v2" "centos-48f11864-957d-4d2e-aa2a-60f4b604f0e7-2" {
  name            = "centos-48f11864-957d-4d2e-aa2a-60f4b604f0e7-2"
  flavor_id       = "3830ebad-ea2f-4822-8a7d-9e301c86a58d"
  key_pair        = "andy-cluster-keypair"
  user_data       = "${file("~/stage-andrew.sh")}"
  image_name      = "CentOS 7.9"
  security_groups = ["f4bc78e0-f25a-4fc1-9808-d0b7125d2155"]

  block_device {
    uuid                  = "48f11864-957d-4d2e-aa2a-60f4b604f0e7"
    source_type           = "image"
    volume_size           = 100
    boot_index            = 0
    destination_type      = "volume"
    delete_on_termination = true
  }

  network {
    uuid  = "0b8fb984-2726-432e-aa37-04b778ef2ba1"
  }
}
    

    
    
resource "openstack_compute_instance_v2" "rocky-b966d2d8-134b-439f-a5de-297f24568bfd-3" {
  name            = "rocky-b966d2d8-134b-439f-a5de-297f24568bfd-3"
  flavor_id       = "3830ebad-ea2f-4822-8a7d-9e301c86a58d"
  key_pair        = "andy-cluster-keypair"
  user_data       = "${file("~/stage-andrew.sh")}"
  image_name      = "Rocky Linux OS 8"
  security_groups = ["f4bc78e0-f25a-4fc1-9808-d0b7125d2155"]

  block_device {
    uuid                  = "b966d2d8-134b-439f-a5de-297f24568bfd"
    source_type           = "image"
    volume_size           = 100
    boot_index            = 0
    destination_type      = "volume"
    delete_on_termination = true
  }

  network {
    uuid  = "0b8fb984-2726-432e-aa37-04b778ef2ba1"
  }
}
    
